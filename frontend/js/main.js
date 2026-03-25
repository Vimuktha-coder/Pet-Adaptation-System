console.log("Multi-Shelter Platform Initialized.");

const API_BASE_URL = "http://localhost:8000";

// API Call Template
async function apiCall(endpoint, method = 'GET', body = null) {
    const options = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) options.body = JSON.stringify(body);
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        return await response.json();
    } catch (e) {
        console.error("API Call error:", e);
        return { error: true, message: "Backend is unreachable." };
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // ---- Volunteer Form ----
    const volunteerForm = document.getElementById("volunteer-form");
    if (volunteerForm) {
        // Fetch registered and approved shelters for the dropdown
        const loadVolunteerShelters = async () => {
            const dropdown = document.getElementById("vol-shelter");
            if (!dropdown) return;

            const res = await apiCall('/admin/shelters');
            if (res.shelters) {
                const approvedShelters = res.shelters.filter(s => s.status === 'APPROVED');
                if (approvedShelters.length === 0) {
                    dropdown.innerHTML = '<option value="">No approved shelters found</option>';
                } else {
                    dropdown.innerHTML = approvedShelters.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
                }
            } else {
                dropdown.innerHTML = '<option value="">Failed to load shelters</option>';
            }
        };
        loadVolunteerShelters();

        volunteerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("vol-name").value;
            const email = document.getElementById("vol-email").value;
            const shelter = document.getElementById("vol-shelter").value;
            const message = document.getElementById("vol-message").value;

            if (!name || !email || !message) return alert("Please fill all required fields.");

            const btn = volunteerForm.querySelector("button");
            const originalText = btn.innerHTML;
            btn.innerHTML = "Submitting...";

            const req = await apiCall('/volunteer/apply', 'POST', { name, email, shelter_id: shelter, message, role: "General Volunteer", user_id: localStorage.getItem("user_id") || null });
            btn.innerHTML = originalText;

            if (req.message) {
                alert("Application submitted successfully!");
                if (req.token) {
                    localStorage.setItem("user_token", req.token);
                    localStorage.setItem("user_role", req.role);
                    localStorage.setItem("user_name", req.user.full_name);
                    localStorage.setItem("user_id", req.user.id);
                }
                window.location.href = "index.html#dashboard";
            } else {
                alert("Submission failed: " + JSON.stringify(req));
            }
        });
    }

    // ---- User Registration Form ----
    const registerUserForm = document.getElementById("register-user-form");
    if (registerUserForm) {
        registerUserForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("reg-user-name").value;
            const email = document.getElementById("reg-user-email").value;
            const password = document.getElementById("reg-user-password").value;
            const role = "USER";

            if (!name || !email || !password) return alert("Please fill all fields.");

            const btn = registerUserForm.querySelector("button");
            const originalText = btn.innerHTML;
            btn.innerHTML = "Processing...";

            const req = await apiCall('/register', 'POST', { name, email, password, role });
            btn.innerHTML = originalText;

            if (req.message) {
                alert("Account created successfully!");
                window.location.href = "login.html";
            } else {
                alert("Creation failed: " + JSON.stringify(req));
            }
        });
    }

    // ---- Shelter Registration Form ----
    const registerShelterForm = document.getElementById("register-shelter-form");
    if (registerShelterForm) {

        registerShelterForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const name = document.getElementById("reg-shelter-name").value;
            const email = document.getElementById("reg-shelter-email").value;
            const phone = document.getElementById("reg-shelter-phone").value;
            const address = document.getElementById("reg-shelter-address").value;
            const description = document.getElementById("reg-shelter-desc").value;
            const password = document.getElementById("reg-shelter-password").value;
            const role = "SHELTER_ADMIN";

            if (!name || !email || !password || !phone || !address || !description) return alert("Please fill all fields.");

            const btn = registerShelterForm.querySelector("button[type='submit']");
            const originalText = btn.innerHTML;
            btn.innerHTML = "Processing...";

            const req = await apiCall('/register', 'POST', {
                name, email, password, role,
                shelter_name: name,
                phone, address, description
            });
            btn.innerHTML = originalText;

            if (req.message) {
                alert("Shelter account created successfully! It is now pending super admin approval.");
                window.location.href = "login.html";
            } else {
                alert("Creation failed: " + JSON.stringify(req));
            }
        });
    }

    // ---- Login Form ----
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("login-email").value;
            const password = document.getElementById("login-password").value;

            if (!email || !password) return alert("Please fill all fields.");

            const btn = loginForm.querySelector("button");
            const originalText = btn.innerHTML;
            btn.innerHTML = "Verifying...";

            const req = await apiCall('/login', 'POST', { email, password });
            btn.innerHTML = originalText;

            if (req.token) {
                alert("Login Successful! Welcome.");
                localStorage.setItem("user_token", req.token);
                localStorage.setItem("user_role", req.role);
                localStorage.setItem("user_name", req.user.full_name);
                localStorage.setItem("user_id", req.user.id);

                // Demo logic for routing
                if (req.role === "SUPER_ADMIN") window.location.href = "admin-dashboard.html";
                else if (req.role === "SHELTER_ADMIN") window.location.href = "shelter-dashboard.html";
                else window.location.href = "index.html#dashboard";

            } else {
                alert("Login failed: " + JSON.stringify(req));
            }
        });
    }

    // ---- Setup Navbar based on Auth State ----
    const updateNavbar = () => {
        // Remove PawPal Chat from navbar universally
        const navLinks = document.querySelector('.nav-links');
        if (navLinks) {
            const chatLink = Array.from(navLinks.querySelectorAll('a')).find(a => a.textContent.includes('PawPal Chat') || a.href.includes('chat.html'));
            if (chatLink) {
                chatLink.remove();
            }
        }

        // Update Auth Buttons
        const navAuth = document.querySelector('.nav-auth');
        const userToken = localStorage.getItem("user_token");
        const userName = localStorage.getItem("user_name") || "Dashboard";
        const userRole = localStorage.getItem("user_role");

        if (navAuth && userToken) {
            let dashboardLink = "index.html#dashboard";
            if (userRole === "SHELTER_ADMIN") dashboardLink = "shelter-dashboard.html";
            else if (userRole === "SUPER_ADMIN") dashboardLink = "admin-dashboard.html";
            else dashboardLink = "index.html#dashboard";

            navAuth.innerHTML = `
                <a href="${dashboardLink}" class="btn btn-secondary" style="background:transparent; border-color:#e5e7eb;">
                    <i class="far fa-user" style="margin-right: 6px;"></i> ${userName.split(' ')[0]}
                </a>
                <button onclick="window.logoutUser()" class="btn btn-secondary" style="border:none; color: var(--text-muted); background: transparent; padding: 10px;">Logout</button>
            `;
        }
    };

    // Run navbar update on DOM load
    updateNavbar();

    window.logoutUser = () => {
        localStorage.clear();
        window.location.href = "index.html";
    };

    // ---- Donate Form ----
    const donateForm = document.getElementById("donate-form");
    if (donateForm) {

        let paymentStatusDiv = document.getElementById("general-payment-status");
        if (!paymentStatusDiv) {
            paymentStatusDiv = document.createElement("div");
            paymentStatusDiv.id = "general-payment-status";
            paymentStatusDiv.style.marginTop = "15px";
            paymentStatusDiv.style.marginBottom = "15px";
            paymentStatusDiv.style.padding = "15px";
            paymentStatusDiv.style.borderRadius = "4px";
            paymentStatusDiv.style.display = "none";
            paymentStatusDiv.style.fontWeight = "600";
            paymentStatusDiv.style.textAlign = "center";
            donateForm.insertBefore(paymentStatusDiv, donateForm.firstChild);
        }

        const showStatus = (msg, isSuccess) => {
            paymentStatusDiv.innerHTML = msg;
            paymentStatusDiv.style.display = "block";
            paymentStatusDiv.style.backgroundColor = isSuccess ? "#E8F5E9" : "#FFEBEE";
            paymentStatusDiv.style.color = isSuccess ? "#2E7D32" : "#C62828";
            paymentStatusDiv.style.border = `1px solid ${isSuccess ? '#C8E6C9' : '#FFCDD2'}`;
        };

        // Check if we just came back from a successful donation
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('success') === 'true') {
            const sessionId = urlParams.get('session_id');
            const btn = document.getElementById('donate-submit-btn');
            if (btn) btn.innerHTML = 'Verifying Payment...';

            if (sessionId) {
                // Verify with backend so it displays on the Admin Dashboard
                apiCall('/verify-payment', 'POST', { session_id: sessionId }).then(res => {
                    if (btn) btn.innerHTML = 'Donate with Stripe';
                    if (!res.error) {
                        showStatus("Thank you! Your Stripe payment was successful and recorded.", true);
                    } else {
                        showStatus("Payment succeeded, but could not be logged to dashboard: " + res.error, false);
                    }
                }).catch(err => {
                    if (btn) btn.innerHTML = 'Donate with Stripe';
                    showStatus("Error verifying payment.", false);
                });
            } else {
                showStatus("Thank you! Your card payment is successful.", true);
            }
            window.history.replaceState({}, document.title, window.location.pathname); // clear URL
        } else if (urlParams.get('canceled') === 'true') {
            showStatus("Payment failed! Stripe checkout was canceled.", false);
            window.history.replaceState({}, document.title, window.location.pathname);
        }

        // Cleaned up UI toggles for custom payment modes since Stripe handles it
        const submitBtn = document.getElementById('donate-submit-btn') || donateForm.querySelector("button");

        if (document.getElementById('donate-amount')) {
            document.getElementById('donate-amount').addEventListener('input', () => { /* No longer needed */ });
        }

        donateForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            paymentStatusDiv.style.display = "none";

            const email = document.getElementById("donate-email").value;
            const amount = document.getElementById("donate-amount").value;

            if (!amount || amount < 1) return showStatus("Please enter a valid amount of at least $1.", false);
            if (!email) return showStatus("Please enter a valid email address.", false);

            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = "Opening Stripe...";

                try {
                    // Fetch Stripe Publishable Key
                    const configReq = await apiCall('/config');
                    if (configReq.error || !configReq.publishableKey) {
                        showStatus("Payment failed! Stripe publishable key not configured on backend.", false);
                        submitBtn.innerHTML = originalText;
                        return;
                    }

                    const stripe = window.Stripe(configReq.publishableKey);

                    const req = await apiCall('/create-checkout-session', 'POST', { amount, email });
                    if (req.sessionId) {
                        // Redirect user to the actual Stripe hosted checkout page via Stripe.js
                        const { error } = await stripe.redirectToCheckout({
                            sessionId: req.sessionId
                        });

                        if (error) {
                            showStatus("Payment failed! Error: " + error.message, false);
                            submitBtn.innerHTML = originalText;
                        }
                    } else {
                        showStatus("Payment failed! Error: " + (req.error || JSON.stringify(req)), false);
                        submitBtn.innerHTML = originalText;
                    }
                } catch (e) {
                    showStatus("Payment failed! Error: " + e.message, false);
                    submitBtn.innerHTML = originalText;
                }
            }
        });
    }

    // ---- Public Pets Page (pets.html) ----
    const publicPetList = document.getElementById("public-pet-list");
    if (publicPetList) {
        window.allPublicPets = [];

        window.loadPublicPets = async () => {
            const res = await apiCall('/pets');
            if (res.pets) {
                // Filter out any pets that are marked 'Adopted' since we only want available ones
                window.allPublicPets = res.pets.filter(p => !p.status || p.status.toLowerCase() !== 'adopted');
                window.renderPublicPets(window.allPublicPets);
            } else {
                publicPetList.innerHTML = '<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: #dc3545;">Failed to load pets. Please try again later.</div>';
            }
        };

        window.renderPublicPets = (petsToRender) => {
            if (petsToRender.length === 0) {
                publicPetList.innerHTML = '<div style="grid-column: 1 / -1; padding: 60px 20px; text-align: center; background: white; border-radius: 12px; border: 1px dashed var(--border);"><p style="color:var(--text-muted); font-size: 1.1rem;">No pets found matching your criteria. Try adjusting your filters!</p></div>';
                return;
            }

            let html = '';
            petsToRender.forEach(p => {
                let imgDisplay = '';
                if (p.image_data) {
                    imgDisplay = `<div style="width: 100%; height: 100%; background-image: url('${p.image_data}'); background-size: cover; background-position: center; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'"></div>`;
                } else if (p.image_name && p.image_name !== 'placeholder.jpg') {
                    imgDisplay = `<div style="width: 100%; height: 100%; background-color: #f1f3f5; display:flex; align-items:center; justify-content:center; color:#999; text-align: center; padding: 20px;">[ Uploaded: ${p.image_name} ]</div>`;
                } else {
                    imgDisplay = `<div style="width: 100%; height: 100%; background-image: url('https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&q=80'); background-size: cover; background-position: center; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'"></div>`;
                }

                html += `
                    <div style="background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); display: flex; flex-direction: column;">
                        <div style="height: 240px; position: relative; overflow: hidden;">
                            <div class="heart-badge" onclick="window.toggleSavePet('${p.id}')" style="position: absolute; top: 15px; right: 15px; background: rgba(255,255,255,0.9); width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 10; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><i class="far fa-heart" onmouseover="this.className='fas fa-heart'; this.style.color='#ea580c'" onmouseout="this.className='far fa-heart'; this.style.color=''"></i></div>
                            ${imgDisplay}
                        </div>
                        <div style="padding: 20px; flex: 1; display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <h3 style="margin: 0; font-size: 1.4rem; color: #ea580c; font-family: 'Playfair Display', serif; font-weight: 700;">${p.name}</h3>
                                ${p.gender ? `<span style="background: #f3f4f6; color: #4b5563; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">${p.gender}</span>` : ''}
                            </div>
                            <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0; margin-bottom: 12px;">${p.age} • ${p.breed || 'Unknown'} • ${p.size || 'Medium'}</p>
                            <p style="color: #4b5563; font-size: 0.9rem; line-height: 1.5; margin-bottom: 20px; flex: 1; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">${p.description || 'A wonderful pet looking for a loving home.'}</p>
                            <a href="pet-details.html?id=${p.id}" style="display: block; text-align: center; border: 1px solid #e5e7eb; padding: 12px; border-radius: 6px; color: #374151; font-weight: 500; font-size: 0.95rem; text-decoration: none; transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='white'">Meet ${p.name}</a>
                        </div>
                    </div>
                `;
            });
            publicPetList.innerHTML = html;
        };

        window.applyPetFilters = () => {
            const search = document.getElementById("filter-search").value.toLowerCase();
            const gender = document.getElementById("filter-gender").value.toLowerCase();
            const size = document.getElementById("filter-size").value.toLowerCase();

            const filtered = window.allPublicPets.filter(p => {
                const pName = (p.name || '').toLowerCase();
                const pBreed = (p.breed || '').toLowerCase();
                const pGender = (p.gender || '').toLowerCase();
                const pSize = (p.size || 'Medium').toLowerCase();

                const matchSearch = pName.includes(search) || pBreed.includes(search);
                const matchGender = gender === "" || pGender === gender;
                const matchSize = size === "" || pSize === size;

                return matchSearch && matchGender && matchSize;
            });

            window.renderPublicPets(filtered);
        };

        // Attach filter functionality
        const filterBtn = document.getElementById("filter-btn");
        if (filterBtn) {
            filterBtn.addEventListener("click", window.applyPetFilters);
        }
        document.getElementById("filter-search").addEventListener("keyup", (e) => {
            if (e.key === 'Enter') window.applyPetFilters();
        });
        document.getElementById("filter-gender").addEventListener("change", window.applyPetFilters);
        document.getElementById("filter-size").addEventListener("change", window.applyPetFilters);

        loadPublicPets(); // Initial load
    }

    // ---- Featured Pets (index.html) ----
    const featuredPetsList = document.getElementById("featured-pets-list");
    if (featuredPetsList) {
        async function loadFeaturedPets() {
            const res = await apiCall('/pets');
            if (res.pets) {
                // Filter for available pets, and take the last 3 (most recently added if IDs are incremental, or reverse them)
                const availablePets = res.pets.filter(p => !p.status || p.status.toLowerCase() !== 'adopted');
                const featured = availablePets.reverse().slice(0, 3);

                if (featured.length === 0) {
                    featuredPetsList.innerHTML = '<p style="color:var(--text-muted); grid-column: 1 / -1; text-align: center;">No featured pets available at the moment.</p>';
                    return;
                }

                let html = '';
                featured.forEach(p => {
                    const imgDisplay = p.image_data
                        ? `url('${p.image_data}')`
                        : (p.image_name && p.image_name !== 'placeholder.jpg'
                            ? 'none' // Usually wouldn't happen for featured
                            : `url('https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&q=80')`);

                    const imgStyle = p.image_data || !p.image_name || p.image_name === 'placeholder.jpg'
                        ? `background-image: ${imgDisplay};`
                        : `background-color: #f1f3f5;`;

                    const placeholderText = (p.image_name && p.image_name !== 'placeholder.jpg' && !p.image_data)
                        ? `[ Uploaded: ${p.image_name} ]` : '';

                    html += `
                        <div class="pet-card">
                            <div class="pet-img" style="${imgStyle} display:flex; align-items:center; justify-content:center; color:#999;">${placeholderText}</div>
                            <div class="pet-info">
                                <h3>${p.name}</h3>
                                <p>${p.age} • ${p.breed}</p>
                                <a href="pet-details.html?id=${p.id}" class="btn btn-secondary full-width">Meet ${p.name}</a>
                            </div>
                        </div>
                    `;
                });
                featuredPetsList.innerHTML = html;
            } else {
                featuredPetsList.innerHTML = '<p style="color:#dc3545; grid-column: 1 / -1; text-align: center;">Failed to load featured pets.</p>';
            }
        }
        loadFeaturedPets();
    }

    // ---- Pet Details Page (pet-details.html) ----
    const petDetailContainer = document.getElementById("pet-detail-container");
    if (petDetailContainer) {
        const urlParams = new URLSearchParams(window.location.search);
        const petId = urlParams.get('id');

        if (!petId) {
            petDetailContainer.innerHTML = '<div style="padding: 40px; text-align: center; color: #dc3545;">No pet ID provided.</div>';
        } else {
            async function loadPetDetails() {
                const res = await apiCall(`/pets/${petId}`);
                if (res.pet) {
                    const p = res.pet;
                    const imgDisplay = p.image_data
                        ? `<div style="flex: 1; background-image: url('${p.image_data}'); background-size: cover; background-position: center; min-height: 500px;"></div>`
                        : p.image_name && p.image_name !== 'placeholder.jpg'
                            ? `<div style="flex: 1; background-color: #f1f3f5; display:flex; align-items:center; justify-content:center; color:#999; border-right: 1px solid var(--border); font-size: 1.2rem;">[ Uploaded: ${p.image_name} ]</div>`
                            : `<div style="flex: 1; background-image: url('https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&q=80'); background-size: cover; background-position: center; min-height: 500px;"></div>`;

                    // Check if saved
                    const savedPets = JSON.parse(localStorage.getItem("saved_pets") || "[]");
                    const isSaved = savedPets.includes(p.id.toString());
                    const savedText = isSaved ? "❤️ Saved" : "🤍 Save Favorite";

                    petDetailContainer.innerHTML = `
                         <div style="background: white; border-radius: 16px; overflow: hidden; display: flex; flex-direction: row; box-shadow: var(--shadow-md); border: 1px solid var(--border); min-height: 500px; flex-wrap: wrap;">
                            ${imgDisplay}
                            <div style="flex: 1; padding: 50px; min-width: 300px;">
                                <div style="display:flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                    <div style="display:inline-block; padding: 4px 12px; background: #fff0eb; color: var(--primary); border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Available for Adoption</div>
                                    <button class="btn btn-secondary" id="save-pet-btn" style="padding: 6px 12px; font-size: 0.9rem;" onclick="window.toggleSavePet('${p.id}')">${savedText}</button>
                                </div>
                                <h1 style="color: var(--primary); font-size: 2.5rem; margin-bottom: 5px;">${p.name}</h1>
                                
                                <div style="margin: 30px 0; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; background: var(--bg-light); padding: 25px; border-radius: 12px; border: 1px solid var(--border);">
                                    <div><p style="color: var(--text-muted); font-size: 0.9rem;">Age</p><p style="font-weight: 600; font-size: 1.1rem; margin-top: 5px;">${p.age}</p></div>
                                    <div><p style="color: var(--text-muted); font-size: 0.9rem;">Breed</p><p style="font-weight: 600; font-size: 1.1rem; margin-top: 5px;">${p.breed}</p></div>
                                    <div><p style="color: var(--text-muted); font-size: 0.9rem;">Gender</p><p style="font-weight: 600; font-size: 1.1rem; margin-top: 5px;">${p.gender || 'Unknown'}</p></div>
                                    <div><p style="color: var(--text-muted); font-size: 0.9rem;">Vaccinated</p><p style="font-weight: 600; font-size: 1.1rem; margin-top: 5px; color: ${p.is_vaccinated ? '#2E7D32' : 'var(--text-main)'};">${p.is_vaccinated ? 'Yes ✓' : 'Unknown'}</p></div>
                                </div>
                                
                                <h3 style="font-family: 'Inter', sans-serif; margin-bottom: 10px;">About ${p.name}</h3>
                                <p style="color: var(--text-muted); margin-bottom: 40px; line-height: 1.7; font-size: 1.05rem;">
                                    ${p.description || "This beautiful pet is looking for a loving home. They would make a wonderful addition to your family. Reach out to learn more!"}
                                </p>
                                
                                <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                                    <button class="btn btn-primary" style="flex: 1; min-width: 200px; padding: 14px; font-size: 1.05rem;" onclick="window.openAdoptionModal('${p.id}', '${p.name.replace(/'/g, "\\'")}')">Apply to Adopt</button>
                                    <button class="btn btn-secondary" style="flex: 1; min-width: 200px; padding: 14px; font-size: 1.05rem;" onclick="window.openChatWidget(true, '${p.name.replace(/'/g, "\\'")}')">Message Shelter</button>
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    petDetailContainer.innerHTML = '<div style="padding: 40px; text-align: center; color: #dc3545;">Pet not found in database.</div>';
                }
            }
            loadPetDetails();

            // Toggle Save functionality
            window.toggleSavePet = (id) => {
                let savedPets = JSON.parse(localStorage.getItem("saved_pets") || "[]");
                id = id.toString();
                if (savedPets.includes(id)) {
                    savedPets = savedPets.filter(pid => pid !== id);
                } else {
                    savedPets.push(id);
                }
                localStorage.setItem("saved_pets", JSON.stringify(savedPets));
                loadPetDetails(); // Re-render to update button text
            };

            // Adoption Modal
            window.openAdoptionModal = (id, petName) => {
                // Redirecting to adoption page instead of using the modal
                window.location.href = `adoption.html?pet_id=${id}&pet_name=${encodeURIComponent(petName)}`;
            };

            const adoptForm = document.getElementById("adoption-modal-form");
            if (adoptForm) {
                // Keep the old logic just in case it's used elsewhere, but ideally we use the dedicated page now
                adoptForm.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const pet_id = document.getElementById("adopt-pet-id").value;
                    const applicant_name = document.getElementById("adopt-name").value;
                    const message = document.getElementById("adopt-message").value + " | Home: " + document.getElementById("adopt-house").value;

                    const btn = adoptForm.querySelector("button[type='submit']");
                    const ogText = btn.innerHTML;
                    btn.innerHTML = "Submitting...";

                    const req = await apiCall('/shelter/adoptions', 'POST', {
                        pet_id,
                        applicant_name,
                        message
                    });
                    btn.innerHTML = ogText;

                    if (req.message) {
                        alert("Application Submitted Successfully! The shelter will review it shortly.");
                        document.getElementById("adoption-modal").style.display = "none";
                    } else {
                        alert("Failed to submit application: " + (req.error || "Unknown Error"));
                    }
                });
            }
        }
    }

    // ---- Dedicated Adoption Page (adoption.html) ----
    const adoptPageForm = document.getElementById("adopt-page-form");
    if (adoptPageForm) {
        // Extract pet info from URL
        const urlParams = new URLSearchParams(window.location.search);
        const petId = urlParams.get('pet_id');
        const petName = urlParams.get('pet_name');

        if (petId) {
            document.getElementById("adopt-page-pet-id").value = petId;
        }

        if (petName) {
            const subtitle = document.querySelector(".section-subtitle");
            if (subtitle) {
                subtitle.textContent = `Tell us about yourself to adopt ${decodeURIComponent(petName)}.`;
            }
        }

        adoptPageForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const pet_id = document.getElementById("adopt-page-pet-id").value;
            if (!pet_id) {
                alert("No pet selected for adoption. Please browse pets first.");
                return;
            }

            const applicant_name = document.getElementById("adopt-page-name").value;
            const email = document.getElementById("adopt-page-email").value;
            const house = document.getElementById("adopt-page-house").value;
            const experience = document.getElementById("adopt-page-experience").value;
            const reason = document.getElementById("adopt-page-reason").value;

            // Combine fields to put into the 'message' or standard fields the backend expects
            const message = `Email: ${email} | Home: ${house} | Exp: ${experience} | Reason: ${reason}`;

            const btn = adoptPageForm.querySelector("button[type='submit']");
            const originalText = btn.innerHTML;
            btn.innerHTML = "Submitting...";

            try {
                // The backend route is /adoption-request and expects pet_id, shelter_id, user_id, experience, house_type, reason
                // We'll fetch the pet details first to get the shelter_id
                const petRes = await apiCall(`/pets/${pet_id}`);
                const shelter_id = petRes.pet ? petRes.pet.shelter_id : null; // we might need to add shelter_id to pet response if not there

                const req = await apiCall('/adoption-request', 'POST', {
                    pet_id: pet_id,
                    user_id: localStorage.getItem("user_id") || null,
                    shelter_id: petRes.pet ? petRes.pet.shelter_id : 1, // Fallback to 1 if we can't get it
                    experience: experience,
                    house_type: house,
                    reason: reason + ` (Applicant: ${applicant_name}, Email: ${email})`
                });

                btn.innerHTML = originalText;

                if (req.message || req.status === 201) {
                    alert(req.message || "Application Submitted Successfully! The shelter will review it shortly.");
                    if (req.token) {
                        localStorage.setItem("user_token", req.token);
                        localStorage.setItem("user_role", req.role);
                        localStorage.setItem("user_name", req.user.full_name);
                        localStorage.setItem("user_id", req.user.id);
                    }
                    window.location.href = "index.html#dashboard"; // Redirect to dashboard
                } else {
                    alert("Failed to submit application: " + (req.error || JSON.stringify(req)));
                }
            } catch (err) {
                btn.innerHTML = originalText;
                alert("An error occurred during submission.");
                console.error(err);
            }
        });
    }

    // ---- Shelter Dashboard ----
    const adoptionRequestsContainer = document.getElementById("adoption-requests");
    if (adoptionRequestsContainer) {
        async function loadAdoptionRequests() {
            const res = await apiCall('/shelter/adoptions');
            if (res.requests) {
                const pendingCount = res.requests.filter(r => r.status === 'PENDING').length;
                document.getElementById("adoption-count").innerText = res.requests.length;

                // Update Sidebar Badge
                const adoptTab = document.querySelector('[data-tab="adoption-reqs"]');
                if (adoptTab) {
                    // It already has active classes, so let's preserve the base text and append badge
                    adoptTab.innerHTML = '📝 3. Adoption Requests ' + (pendingCount > 0 ? `<span style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; margin-left: auto;">${pendingCount} New</span>` : '');
                }

                if (res.requests.length === 0) {
                    adoptionRequestsContainer.innerHTML = '<div style="background: white; padding: 40px; text-align: center; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);"><p style="color: var(--text-muted);">No pending requests at this time.</p></div>';
                    return;
                }

                let html = '';
                res.requests.forEach(r => {
                    html += `
                        <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); display: flex; justify-content: space-between; align-items: center; gap: 20px;">
                            <div>
                                <h3 style="margin-bottom: 5px; color: var(--primary);">${r.pet_name}</h3>
                                <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 10px;"><strong>Applicant:</strong> ${r.applicant_name}</p>
                                <p style="font-style: italic; color: var(--text-muted); font-size: 0.9rem;">"${r.message}"</p>
                                <span style="display: inline-block; margin-top: 10px; font-size: 0.8rem; font-weight: bold; padding: 3px 8px; border-radius: 4px; background: ${r.status === 'APPROVED' ? '#E8F5E9' : (r.status === 'REJECTED' ? '#FFEBEE' : '#FFF3CD')}; color: ${r.status === 'APPROVED' ? '#2E7D32' : (r.status === 'REJECTED' ? '#C62828' : '#856404')};">Status: ${r.status}</span>
                            </div>
                            <div style="display: flex; gap: 10px; flex-shrink: 0;">
                                ${r.status === 'PENDING' ? `<button class="btn btn-primary" onclick="window.processRequest('${r.id}', 'APPROVED')" style="padding: 10px 20px; font-size: 0.9rem;">Approve</button>` : `<button class="btn btn-secondary" style="padding: 10px 20px; font-size: 0.9rem;" disabled>${r.status === 'APPROVED' ? 'Approved' : 'Rejected'}</button>`}
                                ${r.status === 'PENDING' ? `<button class="btn btn-secondary" onclick="window.processRequest('${r.id}', 'REJECTED')" style="padding: 10px 20px; font-size: 0.9rem; background: transparent; border: 1px solid var(--border); color: #dc3545;">Reject</button>` : ''}
                            </div>
                        </div>
                    `;
                });
                adoptionRequestsContainer.innerHTML = html;
            } else {
                adoptionRequestsContainer.innerHTML = '<div style="color: #dc3545; padding: 20px;">Failed to load requests from database.</div>';
            }
        }

        // Attach logic globally so inline onclick events can find it
        window.processRequest = async (id, status) => {
            const req = await apiCall(`/shelter/adoptions/${id}`, 'PUT', { status });
            if (req.message) {
                alert(req.message);
                loadAdoptionRequests(); // refresh the list
            } else {
                alert("Failed to process request: " + JSON.stringify(req));
            }
        };

        // Initially load
        loadAdoptionRequests();

        // ---- Add Pet Form ----
        const addPetForm = document.getElementById("add-pet-form");
        if (addPetForm) {
            addPetForm.addEventListener("submit", async (e) => {
                e.preventDefault();
                const fileInput = document.getElementById("add-pet-image");
                const image_name = fileInput.files.length > 0 ? fileInput.files[0].name : "placeholder.jpg";

                const getBase64 = (file) => new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = () => resolve(reader.result);
                    reader.onerror = error => reject(error);
                });

                let image_data = null;
                if (fileInput.files.length > 0) {
                    try {
                        image_data = await getBase64(fileInput.files[0]);
                    } catch (err) {
                        console.error("Error reading file:", err);
                    }
                }

                const name = document.getElementById("add-pet-name").value;
                const breed = document.getElementById("add-pet-breed").value;
                const age = document.getElementById("add-pet-age").value;
                const gender = document.getElementById("add-pet-gender").value;
                const size = document.getElementById("add-pet-size").value;
                const is_vaccinated = document.getElementById("add-pet-vaccinated").checked;
                const description = document.getElementById("add-pet-desc").value;

                const btn = addPetForm.querySelector("button");
                const originalText = btn.innerHTML;
                btn.innerHTML = "Adding...";

                const req = await apiCall('/pets', 'POST', { name, breed, age, gender, size, is_vaccinated, description, image_name, image_data });
                btn.innerHTML = originalText;

                if (req.message) {
                    alert(req.message);
                    addPetForm.reset();
                    loadShelterPets(); // Refresh table
                    // Switch to manage pets tab
                    document.querySelector('[data-tab="manage-pets"]').click();
                } else {
                    alert("Failed to add pet.");
                }
            });
        }

        // ---- Manage Pets Data ----
        const managePetsContainer = document.getElementById("shelter-pets-list");
        if (managePetsContainer) {
            window.loadShelterPets = async () => {
                const res = await apiCall('/pets');
                if (res.pets) {
                    if (res.pets.length === 0) {
                        managePetsContainer.innerHTML = '<p style="color:var(--text-muted);">No pets currently listed.</p>';
                        return;
                    }
                    let html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;">';
                    res.pets.forEach(p => {
                        html += `
                            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
                                <div style="height: 140px; ${p.image_data ? `background-image: url('${p.image_data}'); background-size: cover; background-position: center; border:none;` : `background: #f1f3f5; border: 1px dashed #ccc;`} border-radius: 8px; margin-bottom: 15px; display: flex; align-items: center; justify-content: center; overflow: hidden; color: var(--text-muted);">
                                    ${!p.image_data ? `<span style="font-size: 0.85rem;">[ Uploaded: ${p.image_name} ]</span>` : ''}
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px;">
                                    <h3 style="color: var(--primary); margin: 0;">${p.name} <span style="font-size: 0.85rem; color: #666; font-weight: normal;">(${p.gender || 'Unknown'})</span></h3>
                                    <span style="display: inline-block; font-size: 0.75rem; font-weight: bold; padding: 3px 8px; border-radius: 4px; background: #E8F5E9; color: #2E7D32;">${p.status}</span>
                                </div>
                                <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0 0 10px 0;"><strong>Breed:</strong> ${p.breed} | <strong>Age:</strong> ${p.age} | <strong>Size:</strong> ${p.size || 'Unknown'}</p>
                                <p style="color: var(--text-main); font-size: 0.9rem; margin: 0 0 15px 0; line-height: 1.4; flex: 1;">${p.description || 'No description provided.'}</p>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                    ${p.is_vaccinated ? '<span style="color: #0288D1; font-size: 0.8rem; font-weight: 600; background: #E1F5FE; padding: 3px 8px; border-radius: 4px;">✓ Vaccinated</span>' : '<span></span>'}
                                </div>
                                <div style="display: flex; gap: 10px; border-top: 1px solid var(--border); padding-top: 15px; margin-top: auto;">
                                    <button class="btn btn-primary" style="padding: 6px 12px; font-size: 0.8rem; background: #2E7D32;" onclick="window.updatePetStatus('${p.id}', 'Adopted')">Mark Adopted</button>
                                    <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.8rem; color: #dc3545; border-color: #dc3545; background: transparent;" onclick="window.deletePet('${p.id}')">Delete</button>
                                </div>
                            </div>
                        `;
                    });
                    html += '</div>';
                    managePetsContainer.innerHTML = html;
                } else {
                    managePetsContainer.innerHTML = '<p style="color:#dc3545;">Failed to load pets.</p>';
                }
            };

            window.deletePet = async (id) => {
                if (!confirm("Are you sure you want to delete this pet?")) return;
                const req = await apiCall(`/pets/${id}`, 'DELETE');
                if (req.message) {
                    alert(req.message);
                    loadShelterPets();
                }
            };

            window.updatePetStatus = async (id, status) => {
                const req = await apiCall(`/pets/${id}`, 'PUT', { status });
                if (req.message) {
                    alert(req.message);
                    loadShelterPets();
                }
            };

            loadShelterPets(); // Initial load
        }

        // ---- Volunteers Data ----
        const volunteersContainer = document.getElementById("volunteer-requests");
        if (volunteersContainer) {
            async function loadVolunteers() {
                const res = await apiCall('/shelter/volunteers');
                if (res.volunteers) {
                    const pendingCount = res.volunteers.filter(v => v.status === 'PENDING').length;

                    // Update Sidebar Badge
                    const volTab = document.querySelector('[data-tab="volunteers"]');
                    if (volTab) {
                        volTab.innerHTML = '🤝 4. Volunteer Applications ' + (pendingCount > 0 ? `<span style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; margin-left: auto;">${pendingCount} New</span>` : '');
                    }

                    if (res.volunteers.length === 0) {
                        volunteersContainer.innerHTML = '<p style="color: var(--text-muted);">No pending volunteer applications.</p>';
                        return;
                    }

                    let html = '';
                    if (pendingCount > 0) {
                        html += `
                            <div style="background: #FFF3CD; border: 1px solid #ffeeba; color: #856404; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
                                <strong>You have ${pendingCount} new volunteer application(s) to review.</strong>
                            </div>
                        `;
                    }

                    res.volunteers.forEach(v => {
                        html += `
                            <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; margin-bottom: 15px;">
                                <div>
                                    <h3 style="margin: 0 0 5px 0; color: var(--primary);">${v.applicant_name}</h3>
                                    <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0 0 10px 0;"><strong>Role:</strong> ${v.role} | <strong>Email:</strong> ${v.email}</p>
                                    <p style="font-style: italic; color: #555; font-size: 0.9rem; margin: 0 0 10px 0;">"${v.message}"</p>
                                    <span style="font-size: 0.8rem; font-weight: bold; padding: 3px 8px; border-radius: 4px; background: ${v.status === 'APPROVED' ? '#E8F5E9' : (v.status === 'REJECTED' ? '#FFEBEE' : '#FFF3CD')}; color: ${v.status === 'APPROVED' ? '#2E7D32' : (v.status === 'REJECTED' ? '#C62828' : '#856404')};">Status: ${v.status}</span>
                                </div>
                                <div style="display: flex; gap: 10px;">
                                    ${v.status === 'PENDING' ? `<button class="btn btn-primary" onclick="window.processVolunteer('${v.id}', 'APPROVED')" style="padding: 8px 16px; font-size: 0.85rem;">Approve</button>` : `<button class="btn btn-secondary" style="padding: 8px 16px; font-size: 0.85rem;" disabled>${v.status === 'APPROVED' ? 'Approved' : 'Rejected'}</button>`}
                                    ${v.status === 'PENDING' ? `<button class="btn btn-secondary" onclick="window.processVolunteer('${v.id}', 'REJECTED')" style="padding: 8px 16px; font-size: 0.85rem; background: transparent; border: 1px solid var(--border); color: #dc3545;">Reject</button>` : ''}
                                </div>
                            </div>
                        `;
                    });
                    volunteersContainer.innerHTML = html;
                }
            }
            window.processVolunteer = async (id, status) => {
                const req = await apiCall(`/shelter/volunteer-status/${id}`, 'PUT', { status });
                if (req.message) {
                    alert(req.message);
                    loadVolunteers();
                }
            };
            loadVolunteers();
        }

        // ---- Chat Data ----
        const chatContainer = document.getElementById("chat-messages-list");
        if (chatContainer) {
            async function loadChats() {
                const res = await apiCall('/messages/shelter');
                if (res.messages) {
                    if (res.messages.length === 0) {
                        chatContainer.innerHTML = '<p style="color: var(--text-muted);">No chat messages.</p>';
                        return;
                    }
                    let html = '';
                    res.messages.forEach(msg => {
                        const isShelter = msg.sender === "Shelter Admin";
                        html += `
                            <div style="display: flex; flex-direction: column; align-items: ${isShelter ? 'flex-end' : 'flex-start'}; margin-bottom: 10px;">
                                <span style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 4px;">${msg.sender} • ${msg.timestamp}</span>
                                <div style="background: ${isShelter ? 'var(--primary)' : '#f1f3f5'}; color: ${isShelter ? 'white' : 'var(--text-main)'}; padding: 12px 18px; border-radius: 20px; max-width: 70%;">
                                    ${msg.message}
                                </div>
                            </div>
                        `;
                    });
                    chatContainer.innerHTML = `<div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); display: flex; flex-direction: column; gap: 10px;">${html}</div>`;
                }
            }
            loadChats();
        }
    }

    // ---- Admin Dashboard Logic ----
    if (window.location.pathname.includes('admin-dashboard')) {
        // 1. Manage Shelters
        const shelterList = document.getElementById('admin-shelter-list');
        const fundShelterSelect = document.getElementById('fund-shelter-id');

        window.loadAdminShelters = async () => {
            const res = await apiCall('/admin/shelters');
            if (res.shelters) {
                const pendingCount = res.shelters.filter(s => s.status === 'PENDING').length;

                // Update Sidebar Badge
                const shelterTab = document.querySelector('[data-tab="admin-shelters"]');
                if (shelterTab) {
                    shelterTab.innerHTML = `🏢 1. Manage Shelters ${pendingCount > 0 ? `<span style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; margin-left: auto;">${pendingCount} New</span>` : ''}`;
                }

                // Update select dropdown
                let selectHtml = '<option value="">Select a shelter...</option>';
                res.shelters.forEach(s => {
                    if (s.status === 'APPROVED') {
                        selectHtml += `<option value="${s.id}">${s.name} (Available Funds: $${s.funds})</option>`;
                    }
                });
                if (fundShelterSelect) fundShelterSelect.innerHTML = selectHtml;

                // Update List
                if (shelterList) {
                    if (res.shelters.length === 0) {
                        shelterList.innerHTML = '<div style="padding: 40px; text-align: center; border-radius: 12px; border: 1px dashed var(--border);"><p style="color:var(--text-muted); font-size: 1.1rem;">No shelters found in the system.</p></div>';
                        return;
                    }

                    let html = '';
                    if (pendingCount > 0) {
                        html += `
                            <div style="background: #FFF3CD; border: 1px solid #ffeeba; color: #856404; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
                                <strong>You have ${pendingCount} pending shelter registration(s) to review.</strong>
                            </div>
                        `;
                    }

                    html += '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px;">';
                    res.shelters.forEach(s => {
                        const bgStatus = s.status === 'APPROVED' ? '#E8F5E9' : '#FFF3CD';
                        const textStatus = s.status === 'APPROVED' ? '#2E7D32' : '#856404';

                        html += `
                            <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); border-top: 4px solid ${s.status === 'APPROVED' ? '#4CAF50' : '#FFC107'}; box-shadow: var(--shadow-sm); display: flex; flex-direction: column; justify-content: space-between; gap: 15px;">
                                <div>
                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                                        <h3 style="margin: 0; color: var(--text-main); font-size: 1.25rem;">${s.name}</h3>
                                        <span style="padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; background: ${bgStatus}; color: ${textStatus}; border: 1px solid ${bgStatus};">${s.status}</span>
                                    </div>
                                    <div style="background: var(--bg-light); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                                        <p style="margin: 0 0 5px 0; color: var(--text-muted); font-size: 0.85rem;"><strong>Email:</strong> ${s.email}</p>
                                        <p style="margin: 0 0 5px 0; color: var(--text-muted); font-size: 0.85rem;"><strong>Phone:</strong> ${s.phone || 'N/A'}</p>
                                        <p style="margin: 0 0 5px 0; color: var(--text-muted); font-size: 0.85rem;"><strong>Address:</strong> ${s.address || 'N/A'}</p>
                                        <p style="margin: 0; color: var(--text-muted); font-size: 0.85rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;"><strong>Desc:</strong> ${s.description || 'N/A'}</p>
                                    </div>
                                    <p style="margin: 0; color: var(--text-main); font-size: 0.95rem;"><strong>Available Funds:</strong> <span style="color: var(--accent); font-weight: bold;">$${s.funds.toLocaleString()}</span></p>
                                </div>
                                
                                <div style="display: flex; gap: 10px; border-top: 1px solid var(--border); padding-top: 15px;">
                                    ${s.status === 'PENDING' ? `<button class="btn btn-primary" style="flex:1; padding: 10px; font-size:0.9rem;" onclick="window.updateShelterStatus('${s.id}', 'APPROVED')">Approve</button>` : `<button class="btn btn-secondary" style="flex:1; padding: 10px; font-size:0.9rem;" disabled>Approved</button>`}
                                    ${s.status === 'PENDING' ? `<button class="btn btn-secondary" style="flex:1; padding: 10px; font-size:0.9rem; color: #dc3545; border-color: #dc3545;" onclick="window.updateShelterStatus('${s.id}', 'REJECTED')">Reject</button>` : ''}
                                </div>
                            </div>
                        `;
                    });
                    html += '</div>';
                    shelterList.innerHTML = html;
                }
            } else {
                if (shelterList) {
                    shelterList.innerHTML = `<div style="padding: 40px; text-align: center; border-radius: 12px; border: 1px dashed var(--border);"><p style="color:#dc3545; font-size: 1.1rem;">Failed to load shelters: ${res.message || res.error || 'Server error'}</p></div>`;
                }
            }
        };

        window.updateShelterStatus = async (id, status) => {
            const req = await apiCall(`/admin/shelters/${id}`, 'PUT', { status });
            if (req.message) {
                alert(req.message);
                loadAdminShelters();
                loadAdminAnalytics();
            }
        };

        // 2. Manage Pets (Global View)
        const globalPetsList = document.getElementById('admin-global-pets-list');
        window.loadAdminPets = async () => {
            if (!globalPetsList) return;
            const res = await apiCall('/pets');
            if (res.pets) {
                if (res.pets.length === 0) {
                    globalPetsList.innerHTML = '<p style="color:var(--text-muted);">No pets currently listed globally.</p>';
                    return;
                }
                let html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;">';
                res.pets.forEach(p => {
                    const imgStyle = p.image_data
                        ? `background-image: url('${p.image_data}'); background-size: cover; background-position: center;`
                        : (p.image_name && p.image_name !== 'placeholder.jpg')
                            ? `background: #f1f3f5;`
                            : `background-image: url('https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&q=80'); background-size: cover;`;

                    const statusColor = p.status === 'Available' ? '#2E7D32' : p.status === 'Adopted' ? '#1565C0' : '#856404';
                    const statusBg = p.status === 'Available' ? '#E8F5E9' : p.status === 'Adopted' ? '#E3F2FD' : '#FFF3CD';

                    html += `
                        <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); display: flex; flex-direction: column; gap: 10px;">
                            <div style="height: 120px; border-radius: 8px; ${imgStyle}"></div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <h4 style="margin: 0; font-size: 1.1rem; color: var(--primary);">${p.name}</h4>
                                <span style="font-size: 0.75rem; font-weight: bold; padding: 3px 8px; border-radius: 4px; background: ${statusBg}; color: ${statusColor};">${p.status}</span>
                            </div>
                            <p style="margin: 0; font-size: 0.85rem; color: var(--text-muted);">
                                <strong>Breed:</strong> ${p.breed}<br>
                                <strong>Age:</strong> ${p.age} | <strong>Gender:</strong> ${p.gender || 'Unknown'}<br>
                                <strong>Size:</strong> ${p.size || 'Unknown'}
                            </p>
                            ${p.status === 'Pending' ? `
                            <div style="display: flex; gap: 10px; border-top: 1px solid var(--border); padding-top: 15px; margin-top: auto;">
                                <button class="btn btn-primary" style="flex:1; padding: 8px; font-size:0.85rem; background: #2E7D32;" onclick="window.updateGlobalPetStatus(${p.id}, 'Available')">Accept</button>
                                <button class="btn btn-secondary" style="flex:1; padding: 8px; font-size:0.85rem; color: #dc3545; border-color: #dc3545;" onclick="window.updateGlobalPetStatus(${p.id}, 'Rejected')">Reject</button>
                            </div>
                            ` : ''}
                        </div>
                    `;
                });
                html += '</div>';
                globalPetsList.innerHTML = html;
            }
        };

        window.updateGlobalPetStatus = async (id, status) => {
            const req = await apiCall(`/pets/${id}`, 'PUT', { status });
            if (req.message) {
                alert(`Pet status updated to ${status}`);
                loadAdminPets();
                loadAdminAnalytics();
            }
        };

        // 3. Donations Overview
        const donationsList = document.getElementById('admin-donations-list');
        window.loadAdminDonations = async () => {
            if (!donationsList) return;
            const res = await apiCall('/admin/donations');
            if (res.donations) {
                if (res.donations.length === 0) {
                    donationsList.innerHTML = '<p style="color:var(--text-muted);">No donations found.</p>';
                    return;
                }
                let total = 0;
                let html = `
                    <div style="display: flex; gap: 20px; margin-bottom: 25px;">
                         <div style="flex: 1; background: var(--bg-light); padding: 20px; border-radius: 8px; border: 1px solid var(--border);">
                             <p style="margin: 0; color: var(--text-muted); font-size: 0.9rem;">Recent Activity</p>
                             <h3 style="margin: 5px 0 0 0; color: var(--text-main); font-size: 1.5rem;">${res.donations.length} Donations</h3>
                         </div>
                    </div>
                    <div style="background: white; border-radius: 12px; border: 1px solid var(--border); overflow: hidden; box-shadow: var(--shadow-sm);">
                        <table style="width: 100%; border-collapse: collapse; text-align: left;">
                            <thead style="background: var(--bg-light); border-bottom: 1px solid var(--border);">
                                <tr>
                                    <th style="padding: 15px 20px; font-weight: 600; color: var(--text-muted); font-size: 0.9rem;">Donor Name</th>
                                    <th style="padding: 15px 20px; font-weight: 600; color: var(--text-muted); font-size: 0.9rem;">Date</th>
                                    <th style="padding: 15px 20px; font-weight: 600; color: var(--text-muted); font-size: 0.9rem; text-align: right;">Amount (INR)</th>
                                </tr>
                            </thead>
                            <tbody>
                `;

                res.donations.forEach((d, index) => {
                    total += (d.amount || 0);
                    const rowBg = index % 2 === 0 ? 'white' : '#fafafa';
                    html += `
                        <tr style="border-bottom: 1px solid var(--border); background: ${rowBg};">
                            <td style="padding: 15px 20px; font-weight: 500;">${d.donor}</td>
                            <td style="padding: 15px 20px; color: var(--text-muted); font-size: 0.95rem;">${d.date}</td>
                            <td style="padding: 15px 20px; text-align: right; font-weight: bold; color: #2E7D32;">$${d.amount.toLocaleString()}</td>
                        </tr>
                    `;
                });
                html += `
                            </tbody>
                            <tfoot style="background: #E8F5E9; border-top: 2px solid #C8E6C9;">
                                <tr>
                                    <td colspan="2" style="padding: 15px 20px; font-weight: bold; text-align: right; color: #2E7D32;">Total Collected</td>
                                    <td style="padding: 15px 20px; font-weight: bold; text-align: right; color: #2E7D32; font-size: 1.1rem;">$${total.toLocaleString()}</td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                `;
                donationsList.innerHTML = html;
            }
        };

        // 4. Fund Allocation
        const allocateForm = document.getElementById('allocate-funds-form');
        if (allocateForm) {
            allocateForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const shelter_id = document.getElementById('fund-shelter-id').value;
                const amount = document.getElementById('fund-amount').value;
                if (!shelter_id || !amount) return;

                const btn = allocateForm.querySelector('button');
                const orig = btn.innerHTML;
                btn.innerHTML = 'Allocating Funds...';

                const req = await apiCall('/admin/allocate-funds', 'POST', { shelter_id, amount });
                btn.innerHTML = orig;

                if (req.message) {
                    alert(req.message);
                    allocateForm.reset();
                    loadAdminShelters(); // Refresh funds in dropdown
                    loadAdminAnalytics(); // Refresh total if needed
                } else {
                    alert("Allocation failed: " + (req.error || JSON.stringify(req)));
                }
            });
        }

        // 5. System Analytics
        window.loadAdminAnalytics = async () => {
            const res = await apiCall('/admin/analytics');
            if (res.total_donations !== undefined) {
                const elDonations = document.getElementById('stat-donations');
                const elShelters = document.getElementById('stat-shelters');
                const elUsers = document.getElementById('stat-users');
                const elPets = document.getElementById('stat-pets');

                if (elDonations) elDonations.innerText = `$ ${res.total_donations.toLocaleString()}`;
                if (elShelters) elShelters.innerText = res.total_shelters;
                if (elUsers) elUsers.innerText = res.total_users;
                if (elPets) elPets.innerText = res.total_pets;
            }
        };

        // Initialize all admin data
        loadAdminShelters();
        loadAdminPets();
        loadAdminDonations();
        loadAdminAnalytics();
    }

    // ---- Dashboard Tab Navigation ----
    const tabLinks = document.querySelectorAll('.tab-link');
    tabLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sidebar = link.parentElement;

            // Un-activate all in this specific sidebar
            sidebar.querySelectorAll('.tab-link').forEach(l => {
                l.classList.remove('active');
                l.style.background = 'transparent';
                l.style.borderLeft = 'none';
                l.style.color = 'var(--text-main)';
                l.style.fontWeight = '500';
            });

            // Activate the clicked link
            link.classList.add('active');
            let highlightColor = '#fff0eb';
            let borderColor = 'var(--primary)';
            if (window.location.pathname.includes('admin')) {
                highlightColor = '#FCF9EC';
                borderColor = 'var(--accent)'; // Gold for super admin
                link.style.color = '#BFA030';
            } else {
                link.style.color = 'var(--primary)'; // Orange for shelter
            }
            link.style.background = highlightColor;
            link.style.borderLeft = `4px solid ${borderColor}`;
            link.style.fontWeight = '600';

            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(tc => tc.style.display = 'none');

            // Show the target tab content safely
            const targetId = link.getAttribute('data-tab');
            const targetElement = document.getElementById(targetId);
            if (targetElement) targetElement.style.display = 'block';
        });
    });

    // ---- AI Chat Widget Logic ----
    const chatWidgetBtn = document.getElementById("chat-widget-btn");
    const chatWidgetContainer = document.getElementById("chat-widget-container");
    const chatCloseBtn = document.getElementById("chat-close-btn");

    if (chatWidgetBtn && chatWidgetContainer) {

        let chatHistory = []; // In-memory history for current session

        function renderWidgetMessages() {
            const container = document.getElementById('messages-container');
            if (!container) return;

            container.innerHTML = '';
            if (chatHistory.length === 0) {
                container.innerHTML = '<div style="text-align: center; color: #888; margin-top: 2rem; font-size: 0.9rem;">Say hello to start the conversation!</div>';
                return;
            }

            chatHistory.forEach(msg => {
                const div = document.createElement('div');
                const isSent = msg.sender_type === 'user';
                div.className = `msg ${isSent ? 'sent' : 'received'}`;

                const time = msg.time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                let htmlContent = `
                    <div>${msg.content}</div>
                `;

                if (!isSent && msg.options && msg.options.length > 0) {
                    htmlContent += '<div class="chat-options">';
                    msg.options.forEach(opt => {
                        htmlContent += `<button class="chat-option-btn" onclick="window.sendChatOption('${opt}')">${opt}</button>`;
                    });
                    htmlContent += '</div>';
                }

                htmlContent += `<div class="msg-time">${time}</div>`;
                div.innerHTML = htmlContent;
                container.appendChild(div);
            });
            container.scrollTop = container.scrollHeight;
        }

        const chatForm = document.getElementById('chat-form');
        if (chatForm) {
            chatForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const input = document.getElementById('msg-input');
                const content = input.value;
                if (!content.trim()) return;

                // Add user message to UI immediately
                const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                chatHistory.push({ content: content, sender_type: 'user', time: timeStr });
                renderWidgetMessages();
                input.value = '';

                // Add loading indicator
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'msg received';
                loadingDiv.id = 'ai-typing-indicator';
                loadingDiv.innerHTML = '<div><i>Typing...</i></div>';
                document.getElementById('messages-container').appendChild(loadingDiv);
                document.getElementById('messages-container').scrollTop = document.getElementById('messages-container').scrollHeight;

                try {
                    const response = await apiCall('/api/ai-chat', 'POST', { message: content });

                    // Remove loading indicator
                    const typingIndicator = document.getElementById('ai-typing-indicator');
                    if (typingIndicator) typingIndicator.remove();

                    if (response.reply) {
                        chatHistory.push({
                            content: response.reply,
                            sender_type: 'ai',
                            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                            options: response.options || []
                        });
                    } else {
                        chatHistory.push({ content: "Sorry, I am having trouble connecting to the network right now.", sender_type: 'ai', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) });
                    }
                    renderWidgetMessages();
                } catch (err) {
                    const typingIndicator = document.getElementById('ai-typing-indicator');
                    if (typingIndicator) typingIndicator.remove();
                    chatHistory.push({ content: "Error communicating with AI.", sender_type: 'ai', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) });
                    renderWidgetMessages();
                }
            });
        }

        // Global function for preset option buttons
        window.sendChatOption = (optionText) => {
            const input = document.getElementById('msg-input');
            if (input) {
                // Remove this option from all previous messages in history to prevent repeating
                chatHistory.forEach(msg => {
                    if (msg.options) {
                        msg.options = msg.options.filter(opt => opt !== optionText);
                    }
                });
                // Re-render to clear the clicked button locally
                renderWidgetMessages();

                input.value = optionText;
                document.getElementById('chat-form').dispatchEvent(new Event('submit'));
            }
        };

        // Toggle Widget
        window.openChatWidget = function(fromPet=false, petName='') {
            if (chatWidgetContainer) chatWidgetContainer.classList.remove("widget-hidden");
            // Add initial welcome if empty
            if (chatHistory.length === 0) {
                let msgContent = "Hi there! 👋 I am the AI Assistant. Looking for a pet? Ask me what we have available right now!";
                if (fromPet && petName) {
                    msgContent = "Hi there! 👋 Are you interested in " + petName + "? I can tell you more about them, or help you with the adoption process!";
                }
                chatHistory.push({
                    content: msgContent,
                    sender_type: 'ai',
                    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    options: ["Show me cats", "Show me dogs", "How to adopt?", "Volunteer info", "How to donate?"]
                });
            }
            if(window.renderWidgetMessages) window.renderWidgetMessages();
        };

        window.renderWidgetMessages = renderWidgetMessages;

        function closeChatWidget() {
            chatWidgetContainer.classList.add("widget-hidden");
        }

        chatWidgetBtn.addEventListener("click", () => window.openChatWidget(false, ''));
        if (chatCloseBtn) chatCloseBtn.addEventListener("click", closeChatWidget);
    }

    // ---- User Dashboard Logic ----
    const userDashboardSection = document.getElementById("user-dashboard-section");
    if (userDashboardSection) {
        // Show only if logged in and looking at dashboard
        const checkDashboardVisibility = () => {
            const userId = localStorage.getItem("user_id");
            if (userId && window.location.hash === "#dashboard") {
                userDashboardSection.style.display = "block";
                loadUserDashboardData(userId);
                // Scroll to it smoothly if we just navigated
                setTimeout(() => {
                    userDashboardSection.scrollIntoView({ behavior: 'smooth' });
                }, 100);
            } else {
                userDashboardSection.style.display = "none";
            }
        };

        window.addEventListener("hashchange", checkDashboardVisibility);
        checkDashboardVisibility(); // Check on load

        async function loadUserDashboardData(userId) {
            const adoptList = document.getElementById("user-adopt-list");
            const volList = document.getElementById("user-vol-list");

            if (adoptList) adoptList.innerHTML = "<p>Loading adoption applications...</p>";
            if (volList) volList.innerHTML = "<p>Loading volunteer applications...</p>";

            // Fetch Adoptions
            const adoptRes = await apiCall(`/user/adoptions?user_id=${userId}`);
            if (adoptList) {
                if (adoptRes.requests && adoptRes.requests.length > 0) {
                    let html = '<div style="display: grid; gap: 15px;">';
                    adoptRes.requests.forEach(r => {
                        let statusColor = r.status === 'APPROVED' ? '#2E7D32' : r.status === 'REJECTED' ? '#C62828' : '#F57F17';
                        let statusBg = r.status === 'APPROVED' ? '#E8F5E9' : r.status === 'REJECTED' ? '#FFEBEE' : '#FFFDE7';
                        html += `
                            <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h4 style="margin: 0; color: var(--primary);">${r.pet_name}</h4>
                                    <p style="margin: 5px 0 0 0; color: var(--text-muted); font-size: 0.9rem;">"${r.message}"</p>
                                </div>
                                <span style="background: ${statusBg}; color: ${statusColor}; padding: 5px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem;">${r.status}</span>
                            </div>
                        `;
                    });
                    html += '</div>';
                    adoptList.innerHTML = html;
                } else {
                    adoptList.innerHTML = "<p style='color: var(--text-muted);'>You have no adoption applications.</p>";
                }
            }

            // Fetch Volunteers
            const volRes = await apiCall(`/user/volunteers?user_id=${userId}`);
            if (volList) {
                if (volRes.requests && volRes.requests.length > 0) {
                    let html = '<div style="display: grid; gap: 15px;">';
                    volRes.requests.forEach(r => {
                        let statusColor = r.status === 'APPROVED' ? '#2E7D32' : r.status === 'REJECTED' ? '#C62828' : '#F57F17';
                        let statusBg = r.status === 'APPROVED' ? '#E8F5E9' : r.status === 'REJECTED' ? '#FFEBEE' : '#FFFDE7';
                        html += `
                            <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h4 style="margin: 0; color: var(--primary);">Shelter: ${r.shelter_name}</h4>
                                    <p style="margin: 5px 0 0 0; color: var(--text-muted); font-size: 0.9rem;">"${r.message}"</p>
                                </div>
                                <span style="background: ${statusBg}; color: ${statusColor}; padding: 5px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem;">${r.status}</span>
                            </div>
                        `;
                    });
                    html += '</div>';
                    volList.innerHTML = html;
                } else {
                    volList.innerHTML = "<p style='color: var(--text-muted);'>You have no volunteer applications.</p>";
                }
            }
        }
    }
});
