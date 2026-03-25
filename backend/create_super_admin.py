import os
import bcrypt
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv(override=True)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    print("❌ ERROR: Supabase credentials not found in .env")
    exit(1)

supabase: Client = create_client(supabase_url, supabase_key)

print("=== 🛠️ CREATING SUPER ADMIN 🛠️ ===")
email = input("Enter admin email (e.g., admin@example.com): ").strip()
password = input("Enter admin password: ").strip()
name = input("Enter admin full name (e.g., Super Admin): ").strip()

if not email or not password:
    print("❌ Email and password are required!")
    exit(1)

# Check if user already exists
existing = supabase.table('users').select('*').eq('email', email).execute()
if existing.data:
    print(f"⚠️ User with email {email} already exists!")
    # Update to SUPER_ADMIN if they already exist
    supabase.table('users').update({'role': 'SUPER_ADMIN'}).eq('email', email).execute()
    print("✅ Updated existing user to SUPER_ADMIN role.")
    exit(0)

# Hash password
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Insert Super Admin
try:
    result = supabase.table('users').insert({
        'full_name': name if name else 'Super Admin',
        'email': email,
        'password_hash': hashed,
        'role': 'SUPER_ADMIN'
    }).execute()
    
    print(f"\n✅ Successfully created SUPER ADMIN Account!")
    print(f"📧 Email: {email}")
    print(f"🔑 Password: [hidden]")
    print(f"You can now login to the admin dashboard with these credentials.")
except Exception as e:
    print(f"\n❌ Error creating admin: {str(e)}")
