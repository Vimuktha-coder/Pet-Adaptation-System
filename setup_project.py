import os

base_dir = r"c:\Users\vimuk\OneDrive\Desktop\x\Multi-Shelter-Platform"

dirs = [
    "backend",
    "frontend/css",
    "frontend/js",
    "frontend/images",
    "database"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. DATABASE SCHEMA
schema_sql = """-- schema.sql
CREATE TABLE USERS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'USER', -- USER, SHELTER_ADMIN, SUPER_ADMIN
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SHELTERS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES USERS(id),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    description TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    funds_allocated DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE PETS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    shelter_id UUID REFERENCES SHELTERS(id),
    name VARCHAR(255) NOT NULL,
    breed VARCHAR(255),
    age INT,
    gender VARCHAR(50),
    vaccination_status Boolean DEFAULT FALSE,
    personality TEXT,
    health_notes TEXT,
    is_adopted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE PET_IMAGES (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pet_id UUID REFERENCES PETS(id),
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ADOPTION_REQUESTS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pet_id UUID REFERENCES PETS(id),
    user_id UUID REFERENCES USERS(id),
    shelter_id UUID REFERENCES SHELTERS(id),
    experience TEXT,
    house_type VARCHAR(255),
    reason TEXT,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE MESSAGES (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id UUID REFERENCES USERS(id),
    receiver_id UUID REFERENCES USERS(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE DONATIONS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    donor_name VARCHAR(255),
    donor_email VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    razorpay_payment_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'PENDING',
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE VOLUNTEERS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES USERS(id),
    shelter_id UUID REFERENCES SHELTERS(id),
    age INT,
    city VARCHAR(255),
    skills TEXT,
    available_days TEXT,
    animal_experience TEXT,
    motivation_message TEXT,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with open(os.path.join(base_dir, "database", "schema.sql"), "w", encoding="utf-8") as f:
    f.write(schema_sql)

# 2. FLASK BACKEND CODE
app_py = """from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import bcrypt
import razorpay
from dotenv import load_dotenv
# from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
CORS(app)

# Razorpay Client
try:
    razorpay_client = razorpay.Client(auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_KEY_SECRET')))
except Exception as e:
    razorpay_client = None
    print("Warning: Razorpay not configured.", e)

# Supabase Client setup (Uncomment when keys are available)
# supabase_url = os.environ.get("SUPABASE_URL")
# supabase_key = os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(supabase_url, supabase_key)

# ========== 1. AUTH ==========
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    # password hashing example
    # hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    # supabase.table('USERS').insert({'full_name': data['name'], 'email': data['email'], 'password_hash': hashed.decode('utf-8')}).execute()
    return jsonify({"message": "Registration successful"}), 201

@app.route('/login', methods=['POST'])
def login():
    # Login logic with Supabase and Bcrypt
    return jsonify({"message": "Login successful", "token": "dummy-token", "role": "USER"}), 200

# ========== 2. PETS ==========
@app.route('/pets', methods=['GET', 'POST'])
def handle_pets():
    if request.method == 'GET':
        return jsonify({"pets": []}), 200
    else: # POST
        return jsonify({"message": "Pet added"}), 201

@app.route('/pets/<id>', methods=['GET', 'PUT', 'DELETE'])
def pet_detail(id):
    if request.method == 'GET':
        return jsonify({"pet": {"id": id, "name": "Buddy", "breed": "Golden Retriever"}}), 200
    elif request.method == 'PUT':
        return jsonify({"message": "Pet updated"}), 200
    else:
        return jsonify({"message": "Pet deleted"}), 200

# ========== 3. ADOPTION ==========
@app.route('/adoption-request', methods=['POST'])
def adoption_request():
    return jsonify({"message": "Adoption request submitted"}), 201

# ========== 4. CHAT ==========
@app.route('/send-message', methods=['POST'])
def send_message():
    return jsonify({"message": "Message sent"}), 201

@app.route('/messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    return jsonify({"messages": []}), 200

# ========== 5. DONATIONS & RAZORPAY ==========
@app.route('/create-razorpay-order', methods=['POST'])
def create_order():
    if not razorpay_client:
        return jsonify({"error": "Razorpay not configured"}), 500
    data = request.json
    amount = int(data.get('amount', 0)) * 100 # amount in paise
    currency = 'INR'
    payment = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
    return jsonify({"order_id": payment['id']}), 200

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    # Verify razorpay signature here
    return jsonify({"message": "Payment verified"}), 200

# ========== 6. VOLUNTEERS ==========
@app.route('/volunteer/apply', methods=['POST'])
def apply_volunteer():
    return jsonify({"message": "Volunteer application submitted directly to shelter administration"}), 201

@app.route('/shelter/volunteers', methods=['GET'])
def get_volunteers():
    # Get volunteer requests for logged in shelter
    return jsonify({"volunteers": []}), 200

@app.route('/shelter/volunteer-status/<id>', methods=['PUT'])
def update_volunteer_status(id):
    data = request.json # { status: 'ACCEPTED' / 'REJECTED' }
    return jsonify({"message": f"Volunteer status updated to {data.get('status')}"}), 200

# ========== 7. FUND ALLOCATION ==========
@app.route('/admin/allocate-funds', methods=['POST'])
def allocate_funds():
    data = request.json
    # Logic to update shelter's allocated funds from super admin
    return jsonify({"message": f"Funds of {data.get('amount')} allocated to shelter {data.get('shelter_id')} successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
"""

with open(os.path.join(base_dir, "backend", "app.py"), "w", encoding="utf-8") as f:
    f.write(app_py)

# 3. ENVIRONMENT AND DEPLOYMENT
requirements_txt = "Flask==3.0.0\nflask-cors==4.0.0\nsupabase==2.3.0\nrazorpay==1.4.1\nbcrypt==4.1.2\npython-dotenv==1.0.0\n"
with open(os.path.join(base_dir, "backend", "requirements.txt"), "w") as f:
    f.write(requirements_txt)

env_example = "SUPABASE_URL=your_supabase_url\nSUPABASE_KEY=your_supabase_key\nRAZORPAY_KEY_ID=your_razorpay_key_id\nRAZORPAY_KEY_SECRET=your_razorpay_key_secret\n"
with open(os.path.join(base_dir, "backend", ".env.example"), "w") as f:
    f.write(env_example)

deploy_md = """# Deployment Instructions

## Backend (Flask, Python)
1. Hosted on a platform like Render or Heroku.
2. Initialize environment: `pip install -r requirements.txt`
3. Add Environment Variables (`SUPABASE_URL`, `SUPABASE_KEY`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`) to your hosting provider settings.
4. Run: `gunicorn app:app` (Make sure to install gunicorn `pip install gunicorn`)

## Frontend (HTML, CSS, JS)
1. Deploy to Vercel, Netlify, or GitHub Pages.
2. Link the frontend API calls to your deployed Flask Backend URL in `js/main.js`.

## Database (Supabase)
1. Go to Supabase dashboard and run the `database/schema.sql` via the SQL Editor to initialize the tables.
"""
with open(os.path.join(base_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(deploy_md)

# 4. FRONTEND PAGES
html_boilerplates = {
    "index.html": "<header><h1>Volunteer, Donate, Adopt!</h1></header><nav><a href='login.html'>Login</a> | <a href='register.html'>Register</a> | <a href='pets.html'>Adopt</a> | <a href='volunteer.html'>Volunteer</a> | <a href='donate.html'>Donate</a></nav><section class='hero'><p>Welcome to the multi-shelter pet adoption network.</p></section>",
    "pets.html": "<h1>Available Pets</h1><input type='text' id='search' placeholder='Search pets...'><div id='pet-list' class='grid-container'></div>",
    "pet-details.html": "<h1>Meet Buster</h1><div class='details-card'><p>Age: 3</p><p>Breed: Husky</p><button>Adoption Request</button> <button>Chat with Shelter</button></div>",
    "adoption.html": "<h1>Adoption Application</h1><form id='adopt-form'><textarea placeholder='Experience with pets'></textarea><button>Submit Request</button></form>",
    "donate.html": "<h1>Support the Shelters</h1><p>Donations go to the Central Super Admin Fund and are distributed accurately to shelters in need.</p><form id='donate-form'><input type='number' placeholder='Amount (INR)'/><button>Donate with Razorpay</button></form>",
    "volunteer.html": "<h1>Volunteer Application</h1><form id='volunteer-form'><input type='text' placeholder='Full Name'/><select><option>Shelter A</option><option>Shelter B</option></select><textarea placeholder='Skills and Motivation'></textarea><button>Apply</button></form>",
    "chat.html": "<h1>Chat Thread</h1><div id='chat-box' class='chat-history'></div><input type='text' id='msg'/><button>Send</button>",
    "login.html": "<h1>Login Phase</h1><form id='login-form'><input type='email' placeholder='Email'/><input type='password' placeholder='Password'/><button>Login</button></form>",
    "register.html": "<h1>Register Now</h1><form id='register-form'><input type='text' placeholder='Name'/><input type='email' placeholder='Email'/><input type='password' placeholder='Password'/><label>Role:</label><select><option value='user'>Public User</option><option value='shelter'>Shelter Admin</option></select><button>Register</button></form>",
    "shelter-dashboard.html": "<h1>Shelter Dashboard</h1><nav><ul><li>Add/Manage Pets</li><li>View Adoption Requests</li><li>Manage Volunteers</li></ul></nav><div id='dashboard-content'></div>",
    "admin-dashboard.html": "<h1>Super Admin Dashboard</h1><nav><ul><li>Approve Shelters</li><li>Fund Allocation Tool</li><li>System Analytics</li></ul></nav><div id='admin-content'></div>"
}

for filename, content in html_boilerplates.items():
    with open(os.path.join(base_dir, "frontend", filename), "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html>\\n<html lang='en'>\\n<head>\\n    <meta charset='UTF-8'>\\n    <title>{filename.split('.')[0].title()}</title>\\n    <link rel='stylesheet' href='css/style.css'>\\n</head>\\n<body>\\n    <div class='container'>\\n        {content}\\n    </div>\\n    <script src='js/main.js'></script>\\n</body>\\n</html>")

with open(os.path.join(base_dir, "frontend", "css", "style.css"), "w", encoding="utf-8") as f:
    f.write("body { font-family: 'Inter', sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; }\n.container { max-width: 1200px; margin: 0 auto; padding: 20px; }\nnav a { margin-right: 15px; color: #0066cc; text-decoration: none; font-weight: bold; }\nheader { background-color: #2c3e50; color: white; padding: 20px 0; text-align: center; }\n.hero { margin-top: 40px; padding: 50px; background: #ecf0f1; border-radius: 8px; }\nform { display: flex; flex-direction: column; max-width: 400px; gap: 10px; margin-top: 20px; }\ninput, textarea, select { padding: 10px; border: 1px solid #ccc; border-radius: 4px; }\nbutton { padding: 10px 15px; background: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer; }\nbutton:hover { background: #2ecc71; }")

with open(os.path.join(base_dir, "frontend", "js", "main.js"), "w", encoding="utf-8") as f:
    f.write("""console.log("Multi-Shelter Platform Initialized.");

const API_BASE_URL = "http://localhost:5000";

// Example of API call template
async function apiCall(endpoint, method='GET', body=null) {
    const options = { method, headers: { 'Content-Type': 'application/json' }};
    if (body) options.body = JSON.stringify(body);
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    return response.json();
}
""")

print("Project generated successfully!")
