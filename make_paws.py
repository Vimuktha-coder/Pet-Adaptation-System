import os

base_dir = r"c:\Users\vimuk\OneDrive\Desktop\x\Multi-Shelter-Platform\frontend"

css_content = """@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap');

:root {
    --primary: #F26A2E; /* Warm Orange */
    --primary-hover: #D9531E;
    --accent: #D4AF37; /* Gold */
    --bg-light: #FDF9F3; /* Warm off-white */
    --text-main: #333333;
    --text-muted: #666666;
    --white: #FFFFFF;
    --border: #E5E5E5;
    --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
    --radius: 8px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-light);
    color: var(--text-main);
    line-height: 1.6;
}

h1, h2, h3, h4, h5 { font-family: 'Playfair Display', serif; font-weight: 700; color: #1a1a1a; }

a { text-decoration: none; color: inherit; }

/* Navigation */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 5%;
    background: rgba(253, 249, 243, 0.95);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: var(--shadow-sm);
    backdrop-filter: blur(10px);
}
.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.5rem;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    color: var(--text-main);
}
.logo-icon { color: var(--primary); font-size: 1.8rem; }
.nav-links { display: flex; gap: 30px; }
.nav-links a { font-weight: 500; color: var(--text-muted); transition: color 0.3s; }
.nav-links a:hover, .nav-links a.active { color: var(--primary); }
.nav-auth { display: flex; gap: 15px; }

/* Buttons */
.btn {
    padding: 10px 24px;
    border-radius: var(--radius);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    font-size: 1rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.btn-primary { background: var(--primary); color: var(--white); }
.btn-primary:hover { background: var(--primary-hover); transform: translateY(-1px); }
.btn-secondary { background: var(--white); color: var(--text-main); border: 1px solid var(--border); }
.btn-secondary:hover { background: #f5f5f5; }
.btn-accent { background: #EBB04D; color: white; }
.full-width { width: 100%; }

/* Hero Section */
.hero {
    position: relative;
    padding: 120px 5%;
    background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&q=80');
    background-size: cover;
    background-position: center;
    color: var(--white);
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.hero-content {
    max-width: 800px;
}
.hero h1 {
    font-size: 4.5rem;
    line-height: 1.1;
    margin-bottom: 20px;
    color: var(--white);
}
.hero h1 span { color: #EBB04D; }
.hero p {
    font-size: 1.2rem;
    margin-bottom: 40px;
    opacity: 0.9;
    max-width: 600px;
}
.hero-buttons { display: flex; gap: 15px; }

/* Sections */
.section { padding: 80px 5%; text-align: center; }
.section-title { font-size: 2.5rem; margin-bottom: 15px; }
.section-subtitle { color: var(--text-muted); max-width: 600px; margin: 0 auto 50px; }

/* Orange Banner */
.banner { background: linear-gradient(135deg, #F26A2E 0%, #EBB04D 100%); padding: 60px 0; }

/* Container */
.container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }

/* Forms */
.form-wrapper {
    background: var(--white);
    max-width: 600px;
    margin: 40px auto;
    padding: 50px;
    border-radius: 16px;
    box-shadow: var(--shadow-md);
    text-align: center;
}
.form-wrapper h1 { margin-bottom: 10px; }
.form-group { margin-bottom: 20px; text-align: left; }
.form-group label { display: block; font-weight: 500; margin-bottom: 8px; font-size: 0.95rem;}
.form-group input, .form-group textarea, .form-group select {
    width: 100%; padding: 12px 16px; border: 1px solid var(--border); border-radius: var(--radius);
    font-family: inherit; font-size: 1rem; transition: all 0.3s; background: #fafafa;
}
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: var(--primary); background: #fff;}

/* Grid Cards */
.grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; }
.pet-card {
    background: var(--white);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    transition: transform 0.3s, box-shadow 0.3s;
    border: 1px solid var(--border);
}
.pet-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-md); }
.pet-img { height: 280px; background-size: cover; background-position: center; }
.pet-info { padding: 25px; text-align: left; }
.pet-info h3 { font-size: 1.5rem; margin-bottom: 5px; }
.pet-info p { color: var(--text-muted); margin-bottom: 20px; font-size: 0.95rem;}

/* Footer */
footer {
    background: var(--white);
    padding: 60px 5% 30px;
    border-top: 1px solid var(--border);
    margin-top: 50px;
}
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
.footer-col h4 { margin-bottom: 20px; font-family: 'Inter', sans-serif; font-size: 1.1rem;}
.footer-col a, .footer-col p { color: var(--text-muted); display: block; margin-bottom: 10px; font-size: 0.95rem; }
.footer-bottom { text-align: center; color: var(--text-muted); padding-top: 20px; border-top: 1px solid var(--border); font-size: 0.9rem;}

/* Chat & Dashboards simplified */
.chat-container { max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: var(--shadow-md); display: flex; flex-direction: column; height: 600px; border: 1px solid var(--border); }
.chat-header { padding: 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px; font-weight: 600;}
.chat-history { flex: 1; padding: 20px; overflow-y: auto; background: var(--bg-light); display: flex; flex-direction: column; gap: 15px; }
.message { max-width: 70%; padding: 12px 16px; border-radius: 16px; position: relative; font-size: 0.95rem;}
.message.received { background: white; align-self: flex-start; border-bottom-left-radius: 4px; box-shadow: var(--shadow-sm); border: 1px solid var(--border); }
.message.sent { background: var(--primary); color: white; align-self: flex-end; border-bottom-right-radius: 4px; }
.chat-input-area { padding: 20px; background: white; border-top: 1px solid var(--border); display: flex; gap: 10px; }
.chat-input-area input { flex: 1; padding: 12px 20px; border: 1px solid var(--border); border-radius: 24px; outline: none; background: #f5f5f5;}
"""

nav_html = """
<nav class="navbar">
    <a href="index.html" class="logo"><span class="logo-icon">❤️</span> PawsConnect</a>
    <div class="nav-links">
        <a href="index.html">Home</a>
        <a href="pets.html">Pets</a>
        <a href="volunteer.html">Volunteer</a>
        <a href="donate.html">Donate</a>
    </div>
    <div class="nav-auth">
        <a href="login.html" class="btn btn-secondary">Login</a>
        <a href="register.html" class="btn btn-primary">Register</a>
    </div>
</nav>
"""

footer_html = """
<footer>
    <div class="footer-grid">
        <div class="footer-col">
            <div class="logo"><span class="logo-icon">❤️</span> PawsConnect</div>
            <p style="margin-top: 15px;">Connecting loving homes with animals in need. Every pet deserves a family.</p>
        </div>
        <div class="footer-col">
            <h4>Quick Links</h4>
            <a href="pets.html">Browse Pets</a>
            <a href="volunteer.html">Volunteer</a>
            <a href="donate.html">Donate</a>
        </div>
        <div class="footer-col">
            <h4>For Shelters</h4>
            <a href="register.html">Register Shelter</a>
            <a href="login.html">Shelter Login</a>
        </div>
        <div class="footer-col">
            <h4>Contact</h4>
            <p>support@pawsconnect.com</p>
            <p>+91 98765 43210</p>
        </div>
    </div>
    <div class="footer-bottom">
        &copy; 2026 PawsConnect. All rights reserved.
    </div>
</footer>
"""

html_boilerplates = {
    "index.html": f"""
    {nav_html}
    <div class="hero">
        <div class="hero-content">
            <h1>Every Pet Deserves a<br><span>Loving Home</span></h1>
            <p>Connect with shelters, adopt your new best friend, volunteer your time, or donate to make a difference in animal lives.</p>
            <div class="hero-buttons">
                <a href="pets.html" class="btn btn-primary">🐾 Adopt a Pet</a>
                <a href="volunteer.html" class="btn btn-secondary">Volunteer</a>
                <a href="donate.html" class="btn btn-secondary">Donate</a>
            </div>
        </div>
    </div>

    <section class="section">
        <div style="margin-bottom: 20px;"><img src="https://cdn-icons-png.flaticon.com/512/2138/2138241.png" width="40" style="opacity: 0.6"></div>
        <h2 class="section-title">About PawsConnect</h2>
        <p class="section-subtitle">PawsConnect is a platform connecting multiple animal shelters with loving families. We facilitate adoptions, coordinate volunteers, and channel donations to support shelters across the country.</p>
    </section>

    <div class="banner"></div>

    <section class="section">
        <h2 class="section-title">Featured Pets</h2>
        <p class="section-subtitle">These adorable animals are looking for their forever homes</p>
        
        <div class="container grid-container" style="padding-top: 0;">
            <div class="pet-card">
                <div class="pet-img" style="background-image: url('https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&q=80');"></div>
                <div class="pet-info">
                    <h3>Bella</h3>
                    <p>2 Years • Golden Retriever</p>
                    <a href="pet-details.html" class="btn btn-secondary full-width">Meet Bella</a>
                </div>
            </div>
            <div class="pet-card">
                <div class="pet-img" style="background-image: url('https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&q=80');"></div>
                <div class="pet-info">
                    <h3>Oliver</h3>
                    <p>1 Year • Domestic Shorthair</p>
                    <a href="pet-details.html" class="btn btn-secondary full-width">Meet Oliver</a>
                </div>
            </div>
            <div class="pet-card">
                <div class="pet-img" style="background-image: url('https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&q=80');"></div>
                <div class="pet-info">
                    <h3>Charlie</h3>
                    <p>6 Months • Beagle Mix</p>
                    <a href="pet-details.html" class="btn btn-secondary full-width">Meet Charlie</a>
                </div>
            </div>
        </div>
        
        <a href="pets.html" class="btn btn-secondary" style="margin-top: 20px;">View All Pets</a>
    </section>
    
    <section class="section" style="background: var(--white);">
        <h2 class="section-title">Success Stories</h2>
        <p class="section-subtitle">Happy endings made possible by our community</p>
        <!-- Adding some fake success stories -->
        <div class="container grid-container" style="padding-top: 0; max-width: 900px;">
           <div style="background: var(--bg-light); border-radius: 12px; padding: 30px; border: 1px solid var(--border); text-align:left;">
               <p style="font-style: italic; color: var(--text-muted); margin-bottom: 20px;">"PawsConnect made finding our new family member so easy. The shelter was incredibly supportive!"</p>
               <h4 style="font-family: 'Inter', sans-serif;">The Smith Family</h4>
           </div>
           
           <div style="background: var(--bg-light); border-radius: 12px; padding: 30px; border: 1px solid var(--border); text-align:left;">
               <p style="font-style: italic; color: var(--text-muted); margin-bottom: 20px;">"Volunteering through the platform has been the most rewarding experience of my life."</p>
               <h4 style="font-family: 'Inter', sans-serif;">Sarah J.</h4>
           </div>
        </div>
    </section>
    {footer_html}
    """,

    "pets.html": f"""
    {nav_html}
    <div class="section" style="padding-bottom: 20px;">
        <h1 class="section-title">Available Pets</h1>
        <p class="section-subtitle">Find your new best friend from our network of shelters.</p>
    </div>
    <div class="container" style="padding-top: 0;">
        <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); margin-bottom: 40px;">
            <div style="display: flex; gap: 15px; margin-bottom: 0px; flex-wrap: wrap;">
                <input type="text" id="filter-search" placeholder="Search by name or breed..." style="flex:1; min-width: 200px; padding: 12px 20px; border-radius: 8px; border: 1px solid var(--border); outline:none; font-family: inherit;">
                <select id="filter-gender" style="padding: 12px 20px; border-radius: 8px; border: 1px solid var(--border); outline:none; font-family: inherit; background: white;">
                    <option value="">All Genders</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>
                <select id="filter-size" style="padding: 12px 20px; border-radius: 8px; border: 1px solid var(--border); outline:none; font-family: inherit; background: white;">
                    <option value="">All Sizes</option>
                    <option value="Small">Small</option>
                    <option value="Medium">Medium</option>
                    <option value="Large">Large</option>
                </select>
                <button class="btn btn-primary" onclick="window.applyPetFilters()">Filter Pets</button>
            </div>
        </div>
        
        <div class="grid-container" id="public-pet-list">
             <div style="grid-column: 1 / -1; padding: 80px 20px; text-align: center; background: white; border-radius: 12px; border: 1px dashed var(--border);">
                 <p style="color: var(--text-muted); font-size: 1.1rem;">Loading amazing pets for you...</p>
             </div>
        </div>
    </div>
    {footer_html}
    """,

    "donate.html": f"""
    {nav_html}
    <div class="container">
        <div class="form-wrapper">
            <h1>Make a Difference</h1>
            <p class="section-subtitle" style="margin-bottom: 30px;">Your donation helps support shelters across our platform. Funds are distributed centrally to where they are needed most.</p>
            <form id='donate-form'>
                <div class="form-group">
                    <label>Amount (INR)</label>
                    <input type='number' id='donate-amount' placeholder='e.g. 1000' required/>
                </div>
                <button class="btn btn-primary full-width" style="margin-top: 10px;">Donate with Stripe</button>
            </form>
        </div>
    </div>
    {footer_html}
    """,
    
    "volunteer.html": f"""
    {nav_html}
    <div class="container">
        <div class="form-wrapper">
            <h1>Volunteer Application</h1>
            <p class="section-subtitle" style="margin-bottom: 30px;">Offer your time and help shelters directly.</p>
            <form id='volunteer-form'>
                <div class="form-group"><label>Full Name</label><input type='text' placeholder='John Doe'/></div>
                <div class="form-group"><label>Email</label><input type='email' placeholder='john@example.com'/></div>
                <div class="form-group">
                    <label>Select Shelter</label>
                    <select><option>Happy Paws Shelter</option><option>City Animal Rescue</option></select>
                </div>
                <div class="form-group"><label>Skills & Motivation</label><textarea rows="4" placeholder="How can you help?"></textarea></div>
                <button class="btn btn-primary full-width" style="margin-top: 10px;">Apply Now</button>
            </form>
        </div>
    </div>
    {footer_html}
    """,

    "login.html": f"""
    {nav_html}
    <div class="container">
        <div class="form-wrapper">
            <h1>Welcome Back</h1>
            <form id='login-form' style="margin-top: 30px;">
                <div class="form-group"><label>Email</label><input type='email' id='login-email' placeholder='Enter your email' required/></div>
                <div class="form-group"><label>Password</label><input type='password' id='login-password' placeholder='Enter your password' required/></div>
                <button class="btn btn-primary full-width" style="margin-top: 10px;">Sign In</button>
            </form>
            <p style="margin-top: 20px; font-size: 0.95rem; color: var(--text-muted)">Don't have an account? <a href="register.html" style="color: var(--primary); font-weight: 500;">Register here</a></p>
        </div>
    </div>
    {footer_html}
    """,

    "register.html": f"""
    {nav_html}
    <div class="container">
        <div class="form-wrapper">
            <h1>Create Account</h1>
            <form id='register-form' style="margin-top: 30px;">
                <div class="form-group"><label>Full Name or Shelter Name</label><input type='text' id='reg-name' placeholder='Name' required/></div>
                <div class="form-group"><label>Email</label><input type='email' id='reg-email' placeholder='Email' required/></div>
                <div class="form-group"><label>Password</label><input type='password' id='reg-password' placeholder='Password' required/></div>
                <div class="form-group">
                    <label>Account Type</label>
                    <select id='reg-role'><option value='user'>Adopter / Volunteer</option><option value='shelter'>Shelter Administrator</option></select>
                </div>
                <button class="btn btn-primary full-width" style="margin-top: 10px;">Create Account</button>
            </form>
        </div>
    </div>
    {footer_html}
    """,
    "pet-details.html": f"""
    {nav_html}
    <div class="container" id="pet-detail-container">
        <div style="padding: 80px 20px; text-align: center; background: white; border-radius: 16px; border: 1px dashed var(--border);">
             <p style="color: var(--text-muted); font-size: 1.1rem;">Loading pet details...</p>
        </div>
    </div>
    
    <!-- Adoption Request Modal (Hidden by Default) -->
    <div id="adoption-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center;">
        <div style="background: white; padding: 40px; border-radius: 16px; max-width: 500px; width: 90%;">
            <h2 style="font-family: 'Playfair Display', serif; margin-bottom: 20px;">Adoption Application</h2>
            <form id="adoption-modal-form" style="display: flex; flex-direction: column; gap: 15px;">
                <input type="hidden" id="adopt-pet-id">
                <div style="display: flex; flex-direction: column; gap: 5px;">
                    <label style="font-weight: 500;">Your Full Name</label>
                    <input type="text" id="adopt-name" required style="padding: 10px; border-radius: 8px; border: 1px solid var(--border);">
                </div>
                <div style="display: flex; flex-direction: column; gap: 5px;">
                    <label style="font-weight: 500;">House Type</label>
                    <select id="adopt-house" style="padding: 10px; border-radius: 8px; border: 1px solid var(--border); background: white;">
                        <option>House with Yard</option>
                        <option>Apartment</option>
                    </select>
                </div>
                <div style="display: flex; flex-direction: column; gap: 5px;">
                    <label style="font-weight: 500;">Why are you a good fit?</label>
                    <textarea id="adopt-message" rows="4" required style="padding: 10px; border-radius: 8px; border: 1px solid var(--border); resize: vertical;"></textarea>
                </div>
                <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 10px;">
                    <button type="button" class="btn btn-secondary" onclick="document.getElementById('adoption-modal').style.display='none'">Cancel</button>
                    <button type="submit" class="btn btn-primary">Submit Application</button>
                </div>
            </form>
        </div>
    </div>
    </div>
    {footer_html}
    """,
    "adoption.html": f"""
    {nav_html}
    <div class="container">
        <div class="form-wrapper">
             <h1>Adoption Application</h1>
             <p class="section-subtitle" style="margin-bottom: 30px;">Tell us about yourself to adopt Bella.</p>
             <form>
                <div class="form-group"><label>House Type</label><select><option>House with Yard</option><option>Apartment</option></select></div>
                <div class="form-group"><label>Experience with Pets</label><textarea rows="4"></textarea></div>
                <button class="btn btn-primary full-width" style="margin-top: 10px;">Submit Application</button>
             </form>
        </div>
    </div>
    {footer_html}
    """,
    "chat.html": f"""
    {nav_html}
    <div class="container">
       <div class="chat-container">
            <div class="chat-header">
                Happy Paws Shelter
            </div>
            <div id='chat-box' class='chat-history'>
                <div class="message received">
                    Hi! Thanks for reaching out about Bella. How can we help?
                </div>
                <div class="message sent">
                    Hello! Is she still available? I would love to schedule a visit!
                </div>
            </div>
            <div class="chat-input-area">
                <input type='text' id='msg' placeholder="Type your message..."/>
                <button class="btn btn-primary">Send</button>
            </div>
        </div>
    </div>
    {footer_html}
    """,
    "shelter-dashboard.html": f"""
    {nav_html}
    <div class="container" style="display: flex; gap: 30px; align-items: flex-start; max-width: 1400px; padding: 40px 5%;">
        <!-- Sidebar Menu -->
        <div style="width: 280px; background: white; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); overflow: hidden; flex-shrink: 0;">
            <div style="background: var(--bg-light); padding: 25px 20px; border-bottom: 1px solid var(--border);">
                <h3 style="margin:0; font-family: 'Playfair Display', serif; color: var(--primary);">Shelter Dashboard</h3>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 5px;">Happy Paws Shelter</p>
            </div>
            <div id="shelter-sidebar" style="display: flex; flex-direction: column;">
                <a href="#" class="tab-link" data-tab="add-pet" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: var(--text-main); font-weight: 500; transition: 0.3s; display: flex; align-items: center; gap: 10px;">🐾 1. Add Pet</a>
                <a href="#" class="tab-link" data-tab="manage-pets" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: var(--text-main); font-weight: 500; transition: 0.3s; display: flex; align-items: center; gap: 10px;">📋 2. Manage Pets</a>
                <a href="#" class="tab-link active" data-tab="adoption-reqs" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: var(--primary); font-weight: 600; background: #fff0eb; display: flex; align-items: center; gap: 10px; border-left: 4px solid var(--primary);">📝 3. Adoption Requests</a>
                <a href="#" class="tab-link" data-tab="volunteers" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: var(--text-main); font-weight: 500; transition: 0.3s; display: flex; align-items: center; gap: 10px;">🤝 4. Volunteer Applications</a>
                <a href="#" class="tab-link" data-tab="chats" style="padding: 18px 20px; color: var(--text-main); font-weight: 500; transition: 0.3s; display: flex; align-items: center; gap: 10px;">💬 5. Chat Messages</a>
            </div>
        </div>
        
        <!-- Main Content Area -->
        <div style="flex: 1;" id="shelter-content">
            <div id="add-pet" class="tab-content" style="display: none; background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <h2 style="font-family: 'Playfair Display', serif; margin-bottom: 20px;">Add a New Pet</h2>
                <form id="add-pet-form" style="display: flex; flex-direction: column; gap: 20px; max-width: 600px;">
                    <div style="display: flex; flex-direction: column; gap: 8px;">
                        <label style="font-weight: 500; color: var(--text-main);">Pet Image</label>
                        <input type="file" id="add-pet-image" accept="image/*" style="padding: 12px 15px; border: 1px dashed var(--border); border-radius: 8px; font-family: inherit; background: var(--bg-light);">
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 8px;">
                        <label style="font-weight: 500; color: var(--text-main);">Pet Name</label>
                        <input type="text" id="add-pet-name" required placeholder="e.g. Max" style="padding: 12px 15px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit;">
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div style="display: flex; flex-direction: column; gap: 8px;">
                            <label style="font-weight: 500; color: var(--text-main);">Breed</label>
                            <input type="text" id="add-pet-breed" required placeholder="e.g. Golden Retriever" style="padding: 12px 15px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit;">
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 8px;">
                            <label style="font-weight: 500; color: var(--text-main);">Age</label>
                            <input type="text" id="add-pet-age" required placeholder="e.g. 2 Months" style="padding: 12px 15px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit;">
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div style="display: flex; flex-direction: column; gap: 8px;">
                            <label style="font-weight: 500; color: var(--text-main);">Gender</label>
                            <select id="add-pet-gender" required style="padding: 12px 15px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit; background: white;">
                                <option value="">Select Gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                            </select>
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 8px;">
                            <label style="font-weight: 500; color: var(--text-main);">Size</label>
                            <select id="add-pet-size" required style="padding: 12px 15px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit; background: white;">
                                <option value="">Select Size</option>
                                <option value="Small">Small (under 10kg)</option>
                                <option value="Medium">Medium (10-25kg)</option>
                                <option value="Large">Large (over 25kg)</option>
                            </select>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px; margin-top: 5px;">
                        <input type="checkbox" id="add-pet-vaccinated" style="width: 18px; height: 18px; cursor: pointer;">
                        <label for="add-pet-vaccinated" style="font-weight: 500; color: var(--text-main); cursor: pointer;">Fully Vaccinated</label>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 8px;">
                        <label style="font-weight: 500; color: var(--text-main);">Description & Personality</label>
                        <textarea id="add-pet-desc" rows="4" required placeholder="Tell adopters about this pet's personality..." style="padding: 12px 15px; border: 1px solid var(--border); border-radius: 8px; font-family: inherit; resize: vertical;"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary" style="align-self: flex-start; margin-top: 10px; padding: 14px 28px;">Add Pet Listing</button>
                </form>
            </div>
            
            <div id="manage-pets" class="tab-content" style="display: none; background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <h2 style="font-family: 'Playfair Display', serif; margin-bottom: 20px;">Manage Pets</h2>
                <div id="shelter-pets-list" style="display: flex; flex-direction: column; gap: 15px;">
                    <p style="color:var(--text-muted); margin-top:10px;">Loading pets...</p>
                </div>
            </div>
            
            <div id="adoption-reqs" class="tab-content" style="display: block;">
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
                    <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                        <p style="color: var(--text-muted);">Total Pets</p><h2 style="font-family: 'Inter', sans-serif;">24</h2>
                    </div>
                    <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                        <p style="color: var(--text-muted);">Adoption Requests</p><h2 style="font-family: 'Inter', sans-serif;" id="adoption-count">3</h2>
                    </div>
                    <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                        <p style="color: var(--text-muted);">Volunteers</p><h2 style="font-family: 'Inter', sans-serif;">15</h2>
                    </div>
                </div>
                
                <div style="background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 15px; margin-bottom: 25px;">
                        <h2 style="margin: 0; font-family: 'Playfair Display', serif;">Pending Adoption Requests</h2>
                        <span style="background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Live Feed</span>
                    </div>
                    
                    <div id="adoption-requests" style="display: flex; flex-direction: column; gap: 15px;">
                        <div style="background: var(--bg-light); padding: 40px; border-radius: 12px; border: 1px dashed var(--border); text-align: center;">
                             <p style="color: var(--text-muted);">Loading requests from database...</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div id="volunteers" class="tab-content" style="display: none; background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <h2 style="font-family: 'Playfair Display', serif;">Volunteer Applications</h2><p style="color:var(--text-muted); margin-top:10px;">(List of volunteers wanting to help at your shelter will show here)</p>
            </div>
            
            <div id="chats" class="tab-content" style="display: none; background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <h2 style="font-family: 'Playfair Display', serif;">Chat Messages</h2><p style="color:var(--text-muted); margin-top:10px;">(Conversations with adopters will load here)</p>
            </div>
        </div>
    </div>
    {footer_html}
    """,
    "admin-dashboard.html": f"""
    {nav_html}
     <div class="container" style="display: flex; gap: 30px; align-items: flex-start; max-width: 1400px; padding: 40px 5%;">
        <!-- Sidebar Menu -->
        <div style="width: 280px; background: white; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); overflow: hidden; flex-shrink: 0;">
            <div style="background: var(--bg-light); padding: 25px 20px; border-bottom: 1px solid var(--border);">
                <h3 style="margin:0; font-family: 'Playfair Display', serif; color: var(--accent);">Super Admin Dashboard</h3>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 5px;">System Overview</p>
            </div>
            <div id="admin-sidebar" style="display: flex; flex-direction: column;">
                <a href="#" class="tab-link" data-tab="admin-shelters" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: var(--text-main); font-weight: 500; transition: 0.3s; display: flex; align-items: center; gap: 10px;">🏢 1. Manage Shelters</a>
                <a href="#" class="tab-link" data-tab="admin-pets" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: var(--text-main); font-weight: 500; transition: 0.3s; display: flex; align-items: center; gap: 10px;">🐾 2. Manage Pets</a>
                <a href="#" class="tab-link" data-tab="admin-donations" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: var(--text-main); font-weight: 500; transition: 0.3s; display: flex; align-items: center; gap: 10px;">💳 3. Donations Overview</a>
                <a href="#" class="tab-link" data-tab="admin-funds" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: var(--text-main); font-weight: 500; transition: 0.3s; display: flex; align-items: center; gap: 10px;">💰 4. Fund Allocation</a>
                <a href="#" class="tab-link active" data-tab="admin-analytics" style="padding: 18px 20px; border-bottom: 1px solid var(--border); color: #BFA030; font-weight: 600; background: #FCF9EC; display: flex; align-items: center; gap: 10px; border-left: 4px solid var(--accent);">📊 5. System Analytics</a>
            </div>
        </div>
        
        <!-- Main Content Area -->
        <div style="flex: 1;" id="admin-content">
            <div id="admin-shelters" class="tab-content" style="display: none; background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <h2 style="font-family: 'Playfair Display', serif;">Manage Shelters</h2><p style="color:var(--text-muted); margin-top:10px;">(Admin list of all registered shelters on platform)</p>
            </div>
            
            <div id="admin-pets" class="tab-content" style="display: none; background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <h2 style="font-family: 'Playfair Display', serif;">Manage Pets</h2><p style="color:var(--text-muted); margin-top:10px;">(Admin global overview of pets)</p>
            </div>
            
             <div id="admin-donations" class="tab-content" style="display: none; background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <h2 style="font-family: 'Playfair Display', serif;">Donations Overview</h2><p style="color:var(--text-muted); margin-top:10px;">(Stripe logs and incoming donation feed)</p>
            </div>
            
             <div id="admin-funds" class="tab-content" style="display: none; background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                <h2 style="font-family: 'Playfair Display', serif;">Fund Allocation</h2><p style="color:var(--text-muted); margin-top:10px;">(Tools to distribute central funds back to shelters)</p>
            </div>
            
            <div id="admin-analytics" class="tab-content" style="display: block;">
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
                    <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); border-top: 4px solid var(--accent);">
                        <p style="color: var(--text-muted);">Total Donations</p><h2 style="font-family: 'Inter', sans-serif;">$ 145,000</h2>
                    </div>
                    <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                        <p style="color: var(--text-muted);">Registered Shelters</p><h2 style="font-family: 'Inter', sans-serif;">12</h2>
                    </div>
                    <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                        <p style="color: var(--text-muted);">Total Users</p><h2 style="font-family: 'Inter', sans-serif;">1,200</h2>
                    </div>
                </div>
                
                <div style="background: white; padding: 35px; border-radius: 12px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 15px; margin-bottom: 25px;">
                        <h2 style="margin: 0; font-family: 'Playfair Display', serif;">System Analytics</h2>
                        <span style="background: #e3f2fd; color: #1565c0; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Last 30 Days</span>
                    </div>
                    <div style="height: 350px; background: var(--bg-light); border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px dashed var(--border);">
                         <p style="color: var(--text-muted);">Interactive analytics chart and graphs will render here.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {footer_html}
    """
}

# Write CSS
with open(os.path.join(base_dir, "css", "style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)

# Write HTML templates
for filename, content in html_boilerplates.items():
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html>\n<html lang='en'>\n<head>\n    <meta charset='UTF-8'>\n    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n    <title>PawsConnect - {filename.split('.')[0].title()}</title>\n    <link rel='stylesheet' href='css/style.css'>\n</head>\n<body>\n    {content}\n    <script src='js/main.js?v=999'></script>\n</body>\n</html>")

print("Finished applying PawsConnect design.")
