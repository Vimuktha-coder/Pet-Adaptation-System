import os

base_dir = r"c:\Users\vimuk\OneDrive\Desktop\x\Multi-Shelter-Platform\frontend"

html_boilerplates = {
    "index.html": """
    <!-- Hero Section -->
    <header class="main-header">
        <nav class="navbar">
            <div class="logo">🐾 Paws & Homes</div>
            <div class="nav-links">
                <a href="index.html">Home</a>
                <a href="pets.html">Adopt</a>
                <a href="volunteer.html">Volunteer</a>
                <a href="donate.html">Donate</a>
            </div>
            <div class="nav-auth">
                <a href="login.html" class="btn-secondary">Login</a>
                <a href="register.html" class="btn-primary">Sign Up</a>
            </div>
        </nav>
        <div class="hero">
            <h1>Find Your New Best Friend</h1>
            <p>Join our network of shelters to adopt, volunteer, and support animals in need.</p>
            <div class="hero-buttons">
                <a href="pets.html" class="btn-primary">Browse Pets</a>
                <a href="donate.html" class="btn-secondary">Support Us</a>
            </div>
        </div>
    </header>

    <section class="features">
        <div class="feature-card">
            <div class="icon">🐶</div>
            <h3>Adopt</h3>
            <p>Find the perfect pet for your lifestyle from thousands of rescues.</p>
        </div>
        <div class="feature-card">
            <div class="icon">🤝</div>
            <h3>Volunteer</h3>
            <p>Give your time to shelters and make a real difference.</p>
        </div>
        <div class="feature-card">
            <div class="icon">❤️</div>
            <h3>Donate</h3>
            <p>Your contributions help us provide food, medical care, and safe shelters.</p>
        </div>
    </section>
    """,

    "pets.html": """
    <header class="sub-header">
        <nav class="navbar">
            <div class="logo">🐾 Paws & Homes</div>
            <div class="nav-links">
                <a href="index.html">Home</a>
                <a href="pets.html" class="active">Adopt</a>
                <a href="volunteer.html">Volunteer</a>
                <a href="donate.html">Donate</a>
            </div>
            <div class="nav-auth">
                <a href="login.html" class="btn-secondary">Login</a>
            </div>
        </nav>
    </header>
    <main class="container">
        <div class="page-title">
            <h1>Available Pets</h1>
            <p>Meet these wonderful animals waiting for a loving home.</p>
        </div>
        <div class="search-bar">
            <input type='text' id='search' placeholder='Search by breed, age, or name...'>
            <button class="btn-primary">Search</button>
        </div>
        <div id='pet-list' class='grid-container'>
            <!-- Fake Pet Card 1 -->
            <div class="pet-card">
                <div class="pet-img bg-dog-1"></div>
                <div class="pet-info">
                    <h3>Buster</h3>
                    <p>3 Years • Golden Retriever</p>
                    <a href="pet-details.html" class="btn-outline">Meet Buster</a>
                </div>
            </div>
            <!-- Fake Pet Card 2 -->
            <div class="pet-card">
                <div class="pet-img bg-cat-1"></div>
                <div class="pet-info">
                    <h3>Luna</h3>
                    <p>1 Year • Siamese Cat</p>
                    <a href="pet-details.html" class="btn-outline">Meet Luna</a>
                </div>
            </div>
             <!-- Fake Pet Card 3 -->
            <div class="pet-card">
                <div class="pet-img bg-dog-2"></div>
                <div class="pet-info">
                    <h3>Max</h3>
                    <p>2 Months • Husky Mix</p>
                    <a href="pet-details.html" class="btn-outline">Meet Max</a>
                </div>
            </div>
        </div>
    </main>
    """,

    "pet-details.html": """
    <header class="sub-header">
         <nav class="navbar">
            <div class="logo">🐾 Paws & Homes</div>
            <div class="nav-links">
                <a href="index.html">Home</a>
                <a href="pets.html">Adopt</a>
            </div>
        </nav>
    </header>
    <main class="container">
        <div class="pet-details-layout">
            <div class="pet-details-img bg-dog-1"></div>
            <div class="details-card">
                <span class="badge">In Shelter</span>
                <h1>Meet Buster</h1>
                <div class="quick-facts">
                    <p><strong>Age:</strong> 3 Years</p>
                    <p><strong>Breed:</strong> Golden Retriever</p>
                    <p><strong>Gender:</strong> Male</p>
                    <p><strong>Vaccinated:</strong> Yes</p>
                </div>
                <h3>About Buster</h3>
                <p class="description">Buster is a loving and energetic golden retriever who loves to play fetch and go on long walks. He is great with kids and other dogs.</p>
                
                <div class="action-buttons">
                    <button class="btn-primary" onclick="window.location.href='adoption.html'">Apply to Adopt</button> 
                    <button class="btn-secondary" onclick="window.location.href='chat.html'">Chat with Shelter</button>
                </div>
            </div>
        </div>
    </main>
    """,

    "adoption.html": """
    <header class="sub-header">
        <nav class="navbar"><div class="logo">🐾 Paws & Homes</div><div class="nav-links"><a href="index.html">Home</a><a href="pets.html">Adopt</a></div></nav>
    </header>
    <main class="container">
        <div class="form-wrapper">
            <h1>Adoption Application</h1>
            <p>Tell us a bit about yourself to adopt Buster.</p>
            <form id='adopt-form'>
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" placeholder="John Doe">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" placeholder="john@example.com">
                </div>
                <div class="form-group">
                    <label>House Type</label>
                    <select>
                        <option>Apartment</option>
                        <option>House with Yard</option>
                        <option>Townhouse</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Experience with Pets</label>
                    <textarea placeholder='Describe your previous pet experience...' rows="4"></textarea>
                </div>
                <button class="btn-primary full-width">Submit Request</button>
            </form>
        </div>
    </main>
    """,

    "donate.html": """
    <header class="sub-header">
        <nav class="navbar"><div class="logo">🐾 Paws & Homes</div><div class="nav-links"><a href="index.html">Home</a><a href="donate.html" class="active">Donate</a></div></nav>
    </header>
    <main class="container">
        <div class="form-wrapper center-text">
            <h1>Support the Shelters ❤️</h1>
            <p>Donations go to the Central Super Admin Fund and are distributed effectively to shelters in need based on resource requirements.</p>
            
            <div class="donation-tiers">
                <div class="tier">₹500<br><span>Feeds a dog</span></div>
                <div class="tier">₹2000<br><span>Medical care</span></div>
                <div class="tier">₹5000<br><span>Shelter support</span></div>
            </div>

            <form id='donate-form'>
                <div class="form-group">
                    <label>Custom Amount (₹)</label>
                    <input type='number' placeholder='Enter amount...'/>
                </div>
                <button class="btn-primary full-width">Donate with Stripe</button>
            </form>
        </div>
    </main>
    """,

    "volunteer.html": """
    <header class="sub-header">
        <nav class="navbar"><div class="logo">🐾 Paws & Homes</div><div class="nav-links"><a href="index.html">Home</a><a href="volunteer.html" class="active">Volunteer</a></div></nav>
    </header>
    <main class="container">
        <div class="form-wrapper">
            <h1>Volunteer Application</h1>
            <p>Help make a direct impact on the lives of these animals.</p>
            <form id='volunteer-form'>
                <div class="form-group"><label>Full Name</label><input type='text' placeholder='Your Name'/></div>
                <div class="form-group"><label>Email</label><input type='email' placeholder='Your Email'/></div>
                <div class="form-group">
                    <label>Preferred Shelter</label>
                    <select><option>Happy Tails Shelter (LA)</option><option>Rescue Paws (NY)</option></select>
                </div>
                <div class="form-group">
                    <label>Skills & Motivation</label>
                    <textarea placeholder='Why do you want to volunteer? What skills can you offer?' rows="4"></textarea>
                </div>
                <button class="btn-primary full-width">Apply Now</button>
            </form>
        </div>
    </main>
    """,

    "chat.html": """
    <header class="sub-header">
        <nav class="navbar"><div class="logo">🐾 Paws & Homes</div></nav>
    </header>
    <main class="container">
        <div class="chat-container">
            <div class="chat-header">
                <h3>Happy Tails Shelter</h3>
                <span class="status-indicator"></span> Online
            </div>
            <div id='chat-box' class='chat-history'>
                <div class="message received">
                    Hello! Thanks for reaching out about Buster. How can we help?
                    <span class="time">10:00 AM</span>
                </div>
                <div class="message sent">
                    Hi! I am interested in adopting him. Is he good with other dogs?
                    <span class="time">10:05 AM</span>
                </div>
            </div>
            <div class="chat-input-area">
                <input type='text' id='msg' placeholder="Type a message..."/>
                <button class="btn-primary">Send</button>
            </div>
        </div>
    </main>
    """,

    "login.html": """
    <div class="auth-page">
        <div class="form-wrapper">
            <div class="logo center-text">🐾 Paws & Homes</div>
            <h1 class="center-text mt-2">Welcome Back</h1>
            <p class="center-text">Log in to manage your account.</p>
            <form id='login-form'>
                <div class="form-group"><label>Email</label><input type='email' placeholder='Enter your email'/></div>
                <div class="form-group"><label>Password</label><input type='password' placeholder='Enter your password'/></div>
                <button class="btn-primary full-width">Login</button>
                <p class="center-text mt-2">Don't have an account? <a href="register.html">Sign Up</a></p>
            </form>
        </div>
    </div>
    """,

    "register.html": """
    <div class="auth-page">
        <div class="form-wrapper">
             <div class="logo center-text">🐾 Paws & Homes</div>
            <h1 class="center-text mt-2">Create Account</h1>
            <form id='register-form'>
                <div class="form-group"><label>Full Name</label><input type='text' placeholder='Name'/></div>
                <div class="form-group"><label>Email</label><input type='email' placeholder='Email'/></div>
                <div class="form-group"><label>Password</label><input type='password' placeholder='Password'/></div>
                <div class="form-group">
                    <label>Role</label>
                    <select><option value='user'>Public User</option><option value='shelter'>Shelter Admin</option></select>
                </div>
                <button class="btn-primary full-width">Register</button>
                <p class="center-text mt-2">Already have an account? <a href="login.html">Log In</a></p>
            </form>
        </div>
    </div>
    """,

    "shelter-dashboard.html": """
    <div class="dashboard-layout">
        <aside class="sidebar">
            <div class="logo">🐾 ShelterAdmin</div>
            <nav class="side-nav">
                <a href="#" class="active">Overview</a>
                <a href="#">Manage Pets</a>
                <a href="#">Adoption Requests</a>
                <a href="#">Volunteers</a>
            </nav>
        </aside>
        <main class="dashboard-main">
            <header class="dash-header">
                <h2>Welcome, Happy Tails Shelter</h2>
            </header>
            <div class="stats-grid">
                <div class="stat-card"><h3>Available Pets</h3><h2>24</h2></div>
                <div class="stat-card"><h3>Pending Adoptions</h3><h2>8</h2></div>
                <div class="stat-card"><h3>Active Volunteers</h3><h2>12</h2></div>
            </div>
            <div id='dashboard-content' class="mt-2">
                <h3>Recent Activity</h3>
                <div class="glass-panel">No new activity to show.</div>
            </div>
        </main>
    </div>
    """,

    "admin-dashboard.html": """
    <div class="dashboard-layout dark-dash">
        <aside class="sidebar">
            <div class="logo">⚡ SuperAdmin</div>
            <nav class="side-nav">
                <a href="#" class="active">Platform Overview</a>
                <a href="#">Manage Shelters</a>
                <a href="#">Fund Allocation</a>
                <a href="#">System Analytics</a>
            </nav>
        </aside>
        <main class="dashboard-main">
            <header class="dash-header">
                <h2>Central Control Panel</h2>
            </header>
            <div class="stats-grid">
                <div class="stat-card highlight"><h3>Total Donations</h3><h2>₹145,000</h2></div>
                <div class="stat-card"><h3>Registered Shelters</h3><h2>15</h2></div>
                <div class="stat-card"><h3>Platform Users</h3><h2>1,204</h2></div>
            </div>
            <div id='admin-content' class="mt-2">
                 <h3>Pending Shelter Approvals</h3>
                 <div class="glass-panel">All shelters have been reviewed.</div>
            </div>
        </main>
    </div>
    """
}

# The CSS is rewritten directly.
css_content = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500;700&display=swap');

:root {
    --primary: #4F46E5;
    --primary-hover: #4338CA;
    --secondary: #10B981;
    --dark: #111827;
    --light: #F9FAFB;
    --gray: #6B7280;
    --card-bg: rgba(255, 255, 255, 0.9);
    --border: #E5E7EB;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body { 
    font-family: 'Inter', sans-serif; 
    background-color: #F3F4F6; 
    color: var(--dark); 
    line-height: 1.6;
}

h1, h2, h3, h4, .logo { font-family: 'Outfit', sans-serif; }

a { text-decoration: none; color: inherit; }

/* Buttons */
.btn-primary, .btn-secondary, .btn-outline {
    display: inline-block;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    border: none;
    font-family: 'Inter', sans-serif;
}
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--primary-hover); transform: translateY(-2px); box-shadow: var(--shadow); }
.btn-secondary { background: var(--secondary); color: white; }
.btn-secondary:hover { background: #059669; transform: translateY(-2px); box-shadow: var(--shadow); }
.btn-outline { background: transparent; border: 2px solid var(--primary); color: var(--primary); }
.btn-outline:hover { background: var(--primary); color: white; }
.full-width { width: 100%; }

/* Navigation */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 5%;
    max-width: 1400px;
    margin: 0 auto;
}
.logo { font-size: 1.5rem; font-weight: 800; color: var(--primary); }
.nav-links a { margin: 0 15px; font-weight: 500; color: var(--gray); transition: color 0.3s; }
.nav-links a:hover, .nav-links a.active { color: var(--primary); }
.nav-auth { display: flex; gap: 10px; }

/* Headers */
.main-header {
    background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
    position: relative;
    overflow: hidden;
}
.sub-header {
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.hero {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    padding: 100px 20px 140px;
}
.hero h1 { font-size: 4rem; font-weight: 800; line-height: 1.1; margin-bottom: 20px; color: var(--dark); }
.hero p { font-size: 1.2rem; color: var(--gray); margin-bottom: 40px; }
.hero-buttons { display: flex; justify-content: center; gap: 20px; }

/* Home Features */
.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    max-width: 1200px;
    margin: -60px auto 50px;
    padding: 0 20px;
    position: relative;
    z-index: 10;
}
.feature-card {
    background: white;
    padding: 40px 30px;
    border-radius: 16px;
    box-shadow: var(--shadow-lg);
    text-align: center;
    transition: transform 0.3s;
}
.feature-card:hover { transform: translateY(-5px); }
.feature-card .icon { font-size: 3rem; margin-bottom: 20px; }
.feature-card h3 { font-size: 1.5rem; margin-bottom: 15px; }
.feature-card p { color: var(--gray); }

/* Containers & Pages */
.container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
.page-title { text-align: center; margin-bottom: 40px; }
.page-title h1 { font-size: 2.5rem; }
.page-title p { color: var(--gray); font-size: 1.1rem; }

/* Forms */
.form-wrapper {
    background: white;
    max-width: 600px;
    margin: 0 auto;
    padding: 40px;
    border-radius: 16px;
    box-shadow: var(--shadow-lg);
}
.form-group { margin-bottom: 20px; text-align: left; }
.form-group label { display: block; font-weight: 500; margin-bottom: 8px; color: var(--dark); }
.form-group input, .form-group textarea, .form-group select {
    width: 100%; padding: 12px 15px; border: 1px solid var(--border); border-radius: 8px;
    font-family: inherit; font-size: 1rem; transition: border-color 0.3s;
}
.form-group input:focus, .form-group textarea:focus, .form-group select:focus {
    outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

/* Pets Grid */
.search-bar { display: flex; max-width: 600px; margin: 0 auto 40px; gap: 10px; }
.search-bar input { flex: 1; padding: 12px 20px; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem; }
.grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; }
.pet-card {
    background: white; border-radius: 16px; overflow: hidden; box-shadow: var(--shadow);
    transition: all 0.3s;
}
.pet-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-lg); }
.pet-img { height: 250px; background-size: cover; background-position: center; background-color: #e2e8f0; }
.pet-info { padding: 25px; }
.pet-info h3 { font-size: 1.5rem; margin-bottom: 5px; }
.pet-info p { color: var(--gray); margin-bottom: 20px; }
.bg-dog-1 { background-image: url('https://images.unsplash.com/photo-1552053831-71594a27632d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'); }
.bg-cat-1 { background-image: url('https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'); }
.bg-dog-2 { background-image: url('https://images.unsplash.com/photo-1543466835-00a7907e9de1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'); }

/* Pet Details */
.pet-details-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; background: white; border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-lg); }
.pet-details-img { min-height: 400px; background-size: cover; background-position: center; }
.details-card { padding: 40px; }
.badge { background: #E0E7FF; color: var(--primary); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; margin-bottom: 15px; }
.details-card h1 { font-size: 2.5rem; margin-bottom: 20px; }
.quick-facts { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px; background: var(--light); padding: 20px; border-radius: 12px; }
.action-buttons { display: flex; gap: 15px; margin-top: 40px; }

/* Chat */
.chat-container { max-width: 800px; margin: 0 auto; background: white; border-radius: 16px; box-shadow: var(--shadow-lg); overflow: hidden; display: flex; flex-direction: column; height: 600px; }
.chat-header { padding: 20px; background: var(--primary); color: white; border-bottom: 1px solid var(--border); }
.status-indicator { display: inline-block; width: 10px; height: 10px; background: #10B981; border-radius: 50%; margin-right: 5px; }
.chat-history { flex: 1; padding: 20px; overflow-y: auto; background: var(--light); display: flex; flex-direction: column; gap: 15px; }
.message { max-width: 70%; padding: 15px; border-radius: 15px; position: relative; }
.message.received { background: white; align-self: flex-start; border-bottom-left-radius: 0; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
.message.sent { background: var(--primary); color: white; align-self: flex-end; border-bottom-right-radius: 0; }
.time { display: block; font-size: 0.75rem; margin-top: 5px; opacity: 0.7; }
.chat-input-area { padding: 20px; background: white; border-top: 1px solid var(--border); display: flex; gap: 10px; }
.chat-input-area input { flex: 1; padding: 12px 20px; border: 1px solid var(--border); border-radius: 20px; outline: none; }
.chat-input-area input:focus { border-color: var(--primary); }

/* Dashboard */
.dashboard-layout { display: flex; min-height: 100vh; }
.sidebar { width: 250px; background: white; border-right: 1px solid var(--border); padding: 20px 0; }
.sidebar .logo { padding: 0 20px; margin-bottom: 30px; }
.side-nav a { display: block; padding: 15px 20px; color: var(--gray); font-weight: 500; border-left: 3px solid transparent; }
.side-nav a:hover, .side-nav a.active { background: var(--light); color: var(--primary); border-left-color: var(--primary); }
.dashboard-main { flex: 1; padding: 40px; }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }
.stat-card { background: white; padding: 25px; border-radius: 12px; box-shadow: var(--shadow); }
.stat-card h3 { color: var(--gray); font-size: 1rem; font-weight: 500; margin-bottom: 10px; }
.stat-card h2 { font-size: 2.5rem; color: var(--dark); }
.glass-panel { background: white; border-radius: 12px; padding: 30px; box-shadow: var(--shadow); }

/* Utils */
.center-text { text-align: center; }
.mt-2 { margin-top: 20px; }
.donation-tiers { display: flex; gap: 15px; margin: 30px 0; justify-content: center; }
.tier { flex: 1; background: var(--light); border: 2px solid var(--border); padding: 20px 10px; border-radius: 12px; font-size: 1.5rem; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.tier span { font-size: 0.85rem; font-weight: 400; color: var(--gray); }
.tier:hover { border-color: var(--primary); color: var(--primary); background: #EEF2FF; }

/* Auth/Full page forms */
.auth-page { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); padding: 20px; }

/* Admin Dashboard Overrides */
.dark-dash { background: #0F172A; }
.dark-dash .sidebar { background: #1E293B; border-color: #334155; }
.dark-dash .side-nav a { color: #94A3B8; }
.dark-dash .side-nav a:hover, .dark-dash .side-nav a.active { background: #0F172A; color: #38BDF8; border-color: #38BDF8; }
.dark-dash .dashboard-main h2, .dark-dash .dashboard-main h3 { color: white; }
.dark-dash .stat-card { background: #1E293B; }
.dark-dash .stat-card h2 { color: white; }
.dark-dash .glass-panel { background: #1E293B; color: #CBD5E1; }
.dark-dash .logo { color: #38BDF8; }
"""

for filename, content in html_boilerplates.items():
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html>\n<html lang='en'>\n<head>\n    <meta charset='UTF-8'>\n    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n    <title>{filename.split('.')[0].replace('-', ' ').title()} - Multi Shelter Platform</title>\n    <link rel='stylesheet' href='css/style.css'>\n</head>\n<body>\n    {content}\n    <script src='js/main.js'></script>\n</body>\n</html>")

with open(os.path.join(base_dir, "css", "style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)

print("Frontend files regenerated successfully!")
