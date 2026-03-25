from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import bcrypt
import stripe
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

load_dotenv(override=True)

app = Flask(__name__)
CORS(app)

# Stripe Client
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Supabase Client setup
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if supabase_url and supabase_key and supabase_url != "your_supabase_url":
    supabase: Client = create_client(supabase_url, supabase_key)
else:
    supabase = None
    print("Warning: Supabase keys not fully configured.")

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Multi-Shelter Backend API is running successfully on port 8000!"
    }), 200

# ========== 1. AUTH ==========
@app.route('/register', methods=['POST'])
def register():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        data = request.json
        email = data.get('email', '').lower()
        
        # Check if user already exists
        existing = supabase.table('users').select('*').eq('email', email).execute()
        if existing.data:
            return jsonify({"error": "Email already registered"}), 400
            
        hashed = bcrypt.hashpw(data.get('password', '').encode('utf-8'), bcrypt.gensalt())
        role = data.get('role', 'USER')
        
        # Insert new user
        result = supabase.table('users').insert({
            'full_name': data.get('name', 'Unknown User'), 
            'email': email, 
            'password_hash': hashed.decode('utf-8'),
            'role': role
        }).execute()
        
        # If shelter admin, create a shelter entry
        if role == 'SHELTER_ADMIN' and result.data:
            user_id = result.data[0]['id']
            supabase.table('shelters').insert({
                'user_id': user_id,
                'name': data.get('shelter_name', f"{data.get('name', '')} Shelter"),
                'phone': data.get('phone', ''),
                'address': data.get('address', ''),
                'description': data.get('description', ''),
                'is_approved': False
            }).execute()
            
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Mock OTP Storage (In-memory for demo purposes)
import random
MOCK_OTPS = {}

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

@app.route('/send-email-otp', methods=['POST'])
def send_email_otp():
    try:
        data = request.json
        email = data.get('email')
        if not email:
            return jsonify({"error": "Email is required"}), 400
            
        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))
        MOCK_OTPS[email] = otp 
        
        # Check if Email SMTP is configured
        smtp_user = os.environ.get('SMTP_EMAIL')
        smtp_pass = os.environ.get('SMTP_PASSWORD')
        
        if smtp_user and smtp_pass and 'your_' not in smtp_user:
            try:
                import smtplib
                from email.mime.text import MIMEText
                
                msg = MIMEText(f"Your PawsConnect Shelter Registration verification code is: {otp}")
                msg['Subject'] = 'PawsConnect Verification Code'
                msg['From'] = smtp_user
                msg['To'] = email

                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
                server.quit()
                
                print(f"✅ Real Email sent to {email}!")
                return jsonify({"message": "OTP sent successfully! Please check your email inbox (and spam folder)."}), 200
            except Exception as e:
                print(f"❌ Failed to send Real Email: {str(e)}")
                return jsonify({"error": f"Failed to send Email via SMTP: {str(e)}"}), 500
        else:
            # Print to console for the user to see (Mock Fallback)
            print(f"\n===================================")
            print(f"📧 MOCK EMAIL TO {email}")
            print(f"💬 Your PawsConnect verification code is: {otp}")
            print(f"===================================\n")
            
            return jsonify({"error": "Email SMTP Not Configured. Please enter your Gmail App Password in the .env file."}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify-email-otp', methods=['POST'])
def verify_email_otp():
    try:
        data = request.json
        email = data.get('email')
        otp = data.get('otp')
        
        if not email or not otp:
            return jsonify({"error": "Email and OTP are required"}), 400
            
        stored_otp = MOCK_OTPS.get(email)
        
        if stored_otp and stored_otp == str(otp):
            # Clean up after successful verification
            MOCK_OTPS.pop(email, None)
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"error": "Invalid or expired OTP"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        data = request.json
        email = data.get('email', '').lower()
        password = data.get('password', '').encode('utf-8')
        
        response = supabase.table('users').select('*').eq('email', email).execute()
        users = response.data
        
        if not users:
            return jsonify({"error": "Invalid email or password"}), 401
            
        user = users[0]
        hashed_password = user['password_hash'].encode('utf-8')
        
        if bcrypt.checkpw(password, hashed_password):
            # Check for shelter approval
            if user['role'] == 'SHELTER_ADMIN':
                shelter_resp = supabase.table('shelters').select('is_approved').eq('user_id', user['id']).execute()
                if shelter_resp.data and not shelter_resp.data[0].get('is_approved', False):
                    return jsonify({"error": "Your shelter account is pending Super Admin approval."}), 403
                    
            return jsonify({
                "message": "Login successful", 
                "token": "dummy-token", 
                "role": user['role'],
                "user": {
                    "id": user['id'],
                    "name": user['full_name'],
                    "full_name": user['full_name'],
                    "email": user['email']
                }
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== MOCK STATE (Removed) ==========
# Mock state variables (MOCK_PETS, MOCK_ADOPTIONS, etc.) have been replaced with real Supabase database interactions.

# ========== 2. PETS ===========
@app.route('/pets', methods=['GET', 'POST'])
def handle_pets():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
        
    if request.method == 'GET':
        try:
            response = supabase.table('pets').select('*, shelters(name), pet_images(image_url)').execute()
            pets = response.data
            
            # Format the response to match the frontend expectations
            formatted_pets = []
            for pet in pets:
                shelter_name = pet.get('SHELTERS', {}).get('name', 'Unknown Shelter') if pet.get('SHELTERS') else 'Unknown Shelter'
                
                # Fetch image from pet_images if exists
                image_data = "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&q=80"
                if pet.get('pet_images') and len(pet['pet_images']) > 0:
                    image_data = pet['pet_images'][0].get('image_url', image_data)
                
                formatted_pet = {
                    "id": pet['id'],
                    "name": pet['name'],
                    "breed": pet['breed'],
                    "age": f"{pet['age']} Years" if pet['age'] else "Unknown",
                    "status": "Available" if not pet['is_adopted'] else "Adopted",
                    "gender": pet['gender'],
                    "size": "Medium", # Add to schema if needed
                    "is_vaccinated": pet['vaccination_status'],
                    "description": pet['personality'] or pet['health_notes'] or "",
                    "shelter_name": shelter_name,
                    "image_data": image_data
                }
                formatted_pets.append(formatted_pet)
                
            return jsonify({"pets": formatted_pets}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    else: # POST
        try:
            data = request.json
            
            # Note: The frontend needs to pass the actual shelter_id
            # For now, we'll try to get the first shelter as a fallback if not provided
            shelter_id = data.get('shelter_id')
            if not shelter_id:
                shelters_response = supabase.table('shelters').select('id').limit(1).execute()
                if shelters_response.data:
                    shelter_id = shelters_response.data[0]['id']
                else:
                    return jsonify({"error": "No shelter found to associate pet with"}), 400
            
            # Extract numerical age from string (e.g., "Max 5" or "2 Years" -> 2)
            age_str = str(data.get("age", "1"))
            age_num = 1
            import re
            numbers = re.findall(r'\d+', age_str)
            if numbers:
                age_num = int(numbers[0])
            
            new_pet_data = {
                "shelter_id": shelter_id,
                "name": data.get("name"),
                "breed": data.get("breed"),
                "age": age_num,
                "gender": data.get("gender"),
                "vaccination_status": data.get("is_vaccinated", False),
                "personality": data.get("description", ""),
                "is_adopted": False
            }
            
            result = supabase.table('pets').insert(new_pet_data).execute()
            
            # Save base64 image data to pet_images if it exists
            if data.get("image_data") and result.data:
                pet_id = result.data[0]['id']
                supabase.table('pet_images').insert({
                    "pet_id": pet_id,
                    "image_url": data.get("image_data")
                }).execute()
            
            return jsonify({"message": f"{data.get('name')} was successfully added to your shelter!"}), 201
        except Exception as e:
            import traceback
            print("ERROR IN POST /pets:")
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

@app.route('/pets/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def pet_detail(id):
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
        
    if request.method == 'GET':
        try:
            response = supabase.table('pets').select('*, shelters(name), pet_images(image_url)').eq('id', id).execute()
            if not response.data:
                return jsonify({"error": "Pet not found"}), 404
            
            pet = response.data[0]
            shelter_name = pet.get('SHELTERS', {}).get('name', 'Unknown Shelter') if pet.get('SHELTERS') else 'Unknown Shelter'
            
            image_data = "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&q=80"
            if pet.get('pet_images') and len(pet['pet_images']) > 0:
                image_data = pet['pet_images'][0].get('image_url', image_data)
            
            formatted_pet = {
                "id": pet['id'],
                "name": pet['name'],
                "breed": pet['breed'],
                "age": f"{pet['age']} Years" if pet['age'] else "Unknown",
                "status": "Available" if not pet['is_adopted'] else "Adopted",
                "gender": pet['gender'],
                "size": "Medium", # Schema doesn't have size
                "is_vaccinated": pet['vaccination_status'],
                "description": pet['personality'] or pet['health_notes'] or "",
                "shelter_name": shelter_name,
                "image_data": image_data
            }
            return jsonify({"pet": formatted_pet}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    elif request.method == 'PUT':
        try:
            data = request.json
            update_data = {}
            if 'status' in data:
                update_data['is_adopted'] = (data['status'].lower() == 'adopted')
                
            if 'name' in data:
                update_data['name'] = data['name']
                
            if update_data:
                response = supabase.table('pets').update(update_data).eq('id', id).execute()
                if not response.data:
                    return jsonify({"error": "Pet not found"}), 404
                    
            return jsonify({"message": "Pet updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    else: # DELETE
        try:
            # First delete related records (images, adoptions) to avoid foreign key constraints
            supabase.table('pet_images').delete().eq('pet_id', id).execute()
            supabase.table('adoption_requests').delete().eq('pet_id', id).execute()
            
            # Now delete the pet
            response = supabase.table('pets').delete().eq('id', id).execute()
            if not response.data:
                return jsonify({"error": "Pet not found"}), 404
                
            return jsonify({"message": "Pet removed from shelter"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# ========== 3. ADOPTION ==========
@app.route('/adoption-request', methods=['POST'])
def adoption_request():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        data = request.json
        
        user_id = data.get('user_id')
        email = data.get('email', 'anonymous@example.com')
        full_name = "User"
        
        if not user_id:
            # Try to extract email from the reason string "Reason: ... (Applicant: John, Email: john@example.com)"
            import re
            extracted_email = "anonymous@example.com"
            extracted_name = "Anonymous Applicant"
            reason_str = data.get('reason', '')
            
            email_match = re.search(r'Email:\s*([^)]*)', reason_str)
            if email_match:
                extracted_email = email_match.group(1).strip()
            
            name_match = re.search(r'Applicant:\s*([^,]*)', reason_str)
            if name_match:
                extracted_name = name_match.group(1).strip()
                
            email = extracted_email
            full_name = extracted_name

            user_response = supabase.table('users').select('id, full_name').eq('email', extracted_email).execute()
            if user_response.data:
                user_id = user_response.data[0]['id']
                full_name = user_response.data[0]['full_name']
            else:
                import bcrypt
                hashed = bcrypt.hashpw(b'placeholder_pwd_123', bcrypt.gensalt()).decode('utf-8')
                new_user = supabase.table('users').insert({
                    'full_name': extracted_name,
                    'email': extracted_email,
                    'password_hash': hashed,
                    'role': 'USER'
                }).execute()
                if new_user.data:
                    user_id = new_user.data[0]['id']
        else:
            # User is already logged in, fetch their details for the response
            user_response = supabase.table('users').select('full_name, email').eq('id', user_id).execute()
            if user_response.data:
                full_name = user_response.data[0]['full_name']
                email = user_response.data[0]['email']

        # Insert a new request
        result = supabase.table('adoption_requests').insert({
            'pet_id': data.get('pet_id'),
            'user_id': user_id,
            'shelter_id': data.get('shelter_id'),
            'experience': data.get('experience', ''),
            'house_type': data.get('house_type', ''),
            'reason': data.get('reason', ''),
            'status': 'PENDING'
        }).execute()
        
        return jsonify({
            "message": "Adoption request submitted successfully",
            "token": "dummy-token",
            "role": "USER",
            "user": {
                "id": user_id,
                "name": full_name,
                "full_name": full_name,
                "email": email
            }
        }), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/shelter/adoptions', methods=['GET'])
def get_adoptions():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        # Note: We should ideally filter by the logged-in shelter's ID using user token
        # For now, we'll fetch all or filter if a shelter_id is provided in args
        shelter_id = request.args.get('shelter_id')
        
        query = supabase.table('adoption_requests').select('id, status, reason, pets(name, breed), users(full_name, email)')
        if shelter_id:
            query = query.eq('shelter_id', shelter_id)
            
        response = query.execute()
        
        # Format the response to match the dashboard's expectations 
        formatted_requests = []
        for req in response.data:
            pet_name = req.get('pets', {}).get('name', 'Unknown Pet') if req.get('pets') else 'Unknown Pet'
            pet_breed = req.get('pets', {}).get('breed', '') if req.get('pets') else ''
            applicant_name = req.get('users', {}).get('full_name', 'Unknown Applicant') if req.get('users') else 'Unknown Applicant'
            
            full_pet_name = f"{pet_name} ({pet_breed})" if pet_breed else pet_name
            
            formatted_requests.append({
                "id": req['id'],
                "pet_name": full_pet_name,
                "applicant_name": applicant_name,
                "status": req['status'],
                "message": req['reason']
            })
            
        return jsonify({"requests": formatted_requests}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/adoptions', methods=['GET'])
def get_user_adoptions():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        user_id = request.args.get('user_id')
        if not user_id:
             return jsonify({"error": "user_id is required"}), 400
             
        query = supabase.table('adoption_requests').select('id, status, reason, pets(name, breed)').eq('user_id', user_id)
        response = query.execute()
        
        formatted_requests = []
        for req in response.data:
            pet_name = req.get('pets', {}).get('name', 'Unknown Pet') if req.get('pets') else 'Unknown Pet'
            pet_breed = req.get('pets', {}).get('breed', '') if req.get('pets') else ''
            
            full_pet_name = f"{pet_name} ({pet_breed})" if pet_breed else pet_name
            
            formatted_requests.append({
                "id": req['id'],
                "pet_name": full_pet_name,
                "status": req['status'],
                "message": req['reason']
            })
            
        return jsonify({"requests": formatted_requests}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/shelter/adoptions/<string:id>', methods=['PUT'])
def process_adoption(id):
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:    
        data = request.json
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({"error": "Status is required"}), 400
            
        response = supabase.table('adoption_requests').update({'status': new_status}).eq('id', id).execute()
        if not response.data:
            return jsonify({"error": "Request not found"}), 404
            
        # If the request was approved, mark the pet as adopted
        if new_status == 'APPROVED':
            pet_id = response.data[0].get('pet_id')
            if pet_id:
                supabase.table('pets').update({'is_adopted': True}).eq('id', pet_id).execute()
                
        return jsonify({"message": f"Adoption request has been marked as {new_status}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========== 4. CHAT (AI Assistant) ==========
import re

@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        data = request.json
        user_message = data.get('message', '').lower()
        
        if not user_message:
            return jsonify({"reply": "I didn't quite catch that. How can I help you regarding our pets?"}), 200

        # Define Intent Matchers
        intents = {
            "greeting": r'\b(hi|hello|hey|greetings|morning|afternoon|evening|who are you)\b',
            "how_to_adopt": r'\b(how to adopt|adopt a pet|adoption process|want to adopt|how do i adopt|adapt|adapt an animal|adopt an animal)\b',
            "how_to_volunteer": r'\b(how to volunteer|volunteer|help out|volunteer application)\b',
            "how_to_donate": r'\b(how to donate|donate|give money|where does the money go|donation)\b',
            "shelter_registration": r'\b(register my shelter|add my rescue|shelter registration)\b',
            "general_help": r'\b(what is this website|what do you do|help|about pawsconnect|general faq|faq)\b',
            "find_pet": r'\b(all pets|show me all pets|dog|dogs|puppy|puppies|cat|cats|kitten|kittens|breed|breeds|age|young|old|\w+ retriever|\w+ shepherd|beagle|terrier|bulldog|hound|husky|labrador|pug|spaniel|collie|mastiff|poodle|chihuahua|mix|shorthair|longhair|siamese|persian|bengal|sphynx)\b',
            "out_of_scope": r'\b(weather|poem|car|recipe|movie|song|president|joke)\b' # Basic examples of out of scope
        }

        # Determine matched intent (first match wins for simplicity, with out_of_scope checking first)
        matched_intent = None
        if re.search(intents["out_of_scope"], user_message):
             matched_intent = "out_of_scope"
        else:
            for intent_name, regex in intents.items():
                if re.search(regex, user_message):
                    matched_intent = intent_name
                    # Prioritize specific commands over general greetings if both exist
                    if matched_intent != "greeting":
                        break 
        
        reply = ""
        options = []

        if matched_intent == "out_of_scope":
            reply = "I'm sorry, I am a specialized virtual assistant. I can only help with questions related to animal adoption, volunteering, donations, and using the PawsConnect platform. How can I help you with our animals today?"
            options = ["How to adopt?", "Show me dogs", "Show me cats", "How to donate?"]
            return jsonify({"reply": reply, "options": options}), 200
            
        elif matched_intent == "greeting":
            reply = "Hello there! 👋 I'm the PawsConnect Virtual Assistant. I can help you find your perfect furry friend, learn how to adopt, volunteer, donate, or register a shelter. How can I help you today?"
            options = ["How to adopt?", "Show me dogs", "Show me cats", "How to donate?", "Volunteer info"]
            
        elif matched_intent == "how_to_adopt":
            reply = "Adopting a pet is easy! Here are the steps:<br>1. Browse our <b>Pets</b> page to find an animal you love.<br>2. Click 'Meet [Pet]' to view their details.<br>3. Click the <b>'Apply to Adopt'</b> button and fill out the short application.<br>4. The shelter will review your application and contact you directly!<br><br>Are you looking for a specific type of pet to start?"
            options = ["Show me dogs", "Show me cats", "Show me all pets"]
            
        elif matched_intent == "how_to_volunteer":
            reply = "We always need helping hands! 🤝<br>To Volunteer:<br>1. Go to the <b>Volunteer</b> page via the main menu.<br>2. Fill out the application form with your details and the specific shelter you'd like to help.<br>3. The shelter admin will review your application and approve it from their dashboard."
            options = ["How to donate?", "General FAQ"]
            
        elif matched_intent == "how_to_donate":
            reply = "Thank you for your generosity! ❤️<br>You can safely donate by visiting the <b>Donate</b> page. We use Stripe for secure payments. All donations are collected by the platform Super Admin and directly allocated to registered shelters in need to help cover food and medical expenses."
            options = ["How to adopt?", "Volunteer info"]
            
        elif matched_intent == "shelter_registration":
            reply = "We'd love to have your shelter on PawsConnect! 🏢<br>1. Click <b>Register</b> in the top right corner and select 'Shelter'.<br>2. Fill in your shelter's details.<br>3. Verify your email using the OTP code sent to you.<br>4. Wait for our Super Admin to review and <b>approve</b> your account. Once approved, you can log in and manage your pets!"
            options = ["General FAQ"]
            
        elif matched_intent == "general_help":
            reply = "PawsConnect is a platform that connects multiple animal shelters with loving families. We facilitate adoptions, coordinate volunteers, and channel donations to support shelters across the country. Let me know if you'd like to adopt, volunteer, or donate!"
            options = ["How to adopt?", "How to donate?", "Volunteer info"]
            
        elif matched_intent == "find_pet":
            # Fetch all available pets dynamically for queries about finding pets
            response = supabase.table('pets').select('*').eq('is_adopted', False).execute()
            pets = response.data
            
            if 'dog' in user_message or 'puppy' in user_message or 'puppies' in user_message:
                dogs = [p for p in pets if p.get('breed') and ('cat' not in p['breed'].lower() and 'feline' not in p['breed'].lower())]
                reply = "We have many wonderful dogs waiting for a home!<br>"
                if len(dogs) > 0:
                    reply += "Here are some of our available dogs:<br>" + "<br>".join([f"• **{d['name']}** ({d['breed']})" for d in dogs[:5]]) + "<br><br>"
                else:
                    reply += "We don't have any dogs available at the moment.<br>"
                reply += "Check out the <a href='pets.html'>Pets page</a> to see them all!"
                options = ["Show me cats", "How to adopt?"]
                
            elif 'cat' in user_message or 'kitten' in user_message:
                cats = [p for p in pets if p.get('breed') and any(word in p['breed'].lower() for word in ['cat', 'domestic', 'shorthair', 'longhair', 'siamese', 'persian', 'bengal', 'sphynx', 'feline', 'mix'])]
                reply = "Yes! We have beautiful cats waiting for a home.<br>"
                if len(cats) > 0:
                    reply += "Here are some of our available cats:<br>" + "<br>".join([f"• **{c['name']}** ({c['breed']})" for c in cats[:5]]) + "<br><br>"
                else:
                    reply += "We don't have any cats available at the moment.<br>"
                reply += "Please check our <a href='pets.html'>Pets page</a> to browse all our lovely feline friends!"
                options = ["Show me dogs", "How to adopt?"]
                    
            elif 'breed' in user_message or 'what kind' in user_message:
                breeds = list(set([p['breed'] for p in pets if p.get('breed')]))
                if breeds:
                    reply += f"We have quite a variety! Some of the breeds currently available are: {', '.join(breeds[:5])}. "
                    if len(breeds) > 5:
                        reply += "And many more! "
                else:
                    reply += "We have many different mixes and breeds available."
                options = ["Show me dogs", "Show me cats"]
                    
            elif 'age' in user_message or 'young' in user_message or 'old' in user_message:
                reply += "We receive pets of all ages, from playful puppies and kittens to calm senior companions. You can filter by age and size on our <a href='pets.html'>Pets page</a>!"
                options = ["How to adopt?"]
            else:
                # Try specific breed match
                specific_match = [p for p in pets if p.get('breed') and p['breed'].lower() in user_message]
                if specific_match:
                    reply = f"Yes, we have a {specific_match[0]['breed']}! Their name is **{specific_match[0]['name']}** and they are {specific_match[0]['age']} years old. You can search for them on the Pets page!"
                else:
                    reply = "We have many wonderful pets waiting for homes! While I couldn't find that exact match right now, please check our <a href='pets.html'>Pets page</a> to see everyone."
                options = ["Show me dogs", "Show me cats"]

        return jsonify({"reply": reply, "options": options}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ========== 5. DONATIONS & STRIPE ==========
@app.route('/config', methods=['GET'])
def stripe_config():
    return jsonify({
        'publishableKey': os.environ.get('STRIPE_PUBLISHABLE_KEY')
    })

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    if not stripe.api_key:
        print("❌ ERROR: Stripe API key not configured. Status: 500 Internal Server Error")
        return jsonify({"error": "Stripe not configured"}), 500
    try:
        data = request.json
        amount = int(data.get('amount', 0)) * 100 # amount in cents
        
        if amount < 100:
            return jsonify({"error": "Minimum donation amount is $1.00"}), 400
        
        print(f"\n===================================")
        print(f"🔄 INITIATING STRIPE CHECKOUT...")
        print(f"Amount: ${amount/100}")
        if data.get('email'):
            print(f"Email: {data.get('email')}")
        print(f"===================================")
        
        session_kwargs = {
            'payment_method_types': ['card', 'link'],
            'line_items': [{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'PawsConnect Donation',
                        'description': 'Thank you for supporting our animal shelters!',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            'mode': 'payment',
            'success_url': 'http://localhost:8080/donate.html?success=true&session_id={CHECKOUT_SESSION_ID}',
            'cancel_url': 'http://localhost:8080/donate.html?canceled=true',
        }
        
        email = data.get('email')
        if email:
            session_kwargs['customer_email'] = email
            
        session = stripe.checkout.Session.create(**session_kwargs)
        return jsonify({
            'sessionId': session.id
        }), 200
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    session_id = data.get('session_id')
    print(f"\n🔄 VERIFYING PAYMENT FOR SESSION: {session_id}")
    
    if not session_id or not stripe.api_key:
        print(f"❌ ERROR: Invalid request or Stripe not configured. Status: 400 Bad Request")
        return jsonify({"error": "Invalid request or Stripe not configured"}), 400
        
    if not supabase:
        print(f"❌ ERROR: Database not configured. Status: 500 Internal Server Error")
        return jsonify({"error": "Database not configured"}), 500
        
    try:
        print(f"📡 Fetching session details from Stripe API...")
        # Securely retrieve the session from Stripe using the ID
        session = stripe.checkout.Session.retrieve(session_id)
        print(f"📊 STRIPE API RESPONSE: Payment Status is '{session.payment_status}'")
        
        if session.payment_status == 'paid':
            # Check if we already recorded this to prevent duplicate entries on refresh
            existing = supabase.table('donations').select('id').eq('stripe_payment_id', session_id).execute()
            if existing.data:
                print(f"===================================")
                print(f"✅  Stripe Payment Already Recorded")
                print(f"===================================")
                return jsonify({"message": "Payment already verified"}), 200
                    
            amount_in_inr = session.amount_total / 100
            
            # Extract customer info
            donor_name = "Anonymous"
            donor_email = ""
            if session.customer_details:
                if session.customer_details.name:
                    donor_name = session.customer_details.name
                if session.customer_details.email:
                    donor_email = session.customer_details.email
            elif session.customer_email:
                donor_email = session.customer_email
                donor_name = session.customer_email
                
            # Insert the donation
            supabase.table('donations').insert({
                "donor_name": donor_name,
                "donor_email": donor_email,
                "amount": amount_in_inr,
                "stripe_payment_id": session_id,
                "status": "COMPLETED"
            }).execute()
            
            print(f"===================================")
            print(f"💰 STRIPE PAYMENT SUCCESSFUL! 💰")
            print(f"Donor: {donor_name}")
            print(f"Amount: ${amount_in_inr}")
            print(f"Session: {session_id}")
            print(f"✅ Status Code: 200 OK")
            print(f"===================================")
            
            return jsonify({"message": "Payment verified and recorded!"}), 200
        else:
            print(f"⚠️ Payment not completed. Status Code: 400 Bad Request")
            return jsonify({"error": "Payment not completed"}), 400
    except Exception as e:
        print(f"❌ ERROR verifying payment: {str(e)}. Status Code: 500 Internal Server Error")
        return jsonify({"error": str(e)}), 500

# ========== 6. VOLUNTEERS ==========
@app.route('/volunteer/apply', methods=['POST'])
def apply_volunteer():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        data = request.json
        
        # The frontend isn't necessarily sending standard user info, so we might need to 
        # try to find a user id based on email, or just insert the application if allowed
        # Current schema has user_id, but the frontend form might be for anonymous users.
        # Let's insert what we can.
        
        # If no user_id, check if email exists in USERS to get an ID
        user_id = data.get('user_id')
        email = data.get('email')
        full_name = "User"
        
        if not user_id and email:
            user_response = supabase.table('users').select('id, full_name').eq('email', email).execute()
            if user_response.data:
                user_id = user_response.data[0]['id']
                full_name = user_response.data[0]['full_name']
            else:
                # User doesn't exist, create a new one to satisfy the Foreign Key constraint
                import bcrypt
                name = data.get('name', email.split('@')[0])
                full_name = name
                # Provide a random placeholder password
                hashed = bcrypt.hashpw(b'placeholder_pwd_123', bcrypt.gensalt()).decode('utf-8')
                new_user = supabase.table('users').insert({
                    'full_name': name,
                    'email': email,
                    'password_hash': hashed,
                    'role': 'USER'
                }).execute()
                if new_user.data:
                    user_id = new_user.data[0]['id']
        elif user_id:
            user_response = supabase.table('users').select('full_name, email').eq('id', user_id).execute()
            if user_response.data:
                full_name = user_response.data[0]['full_name']
                email = user_response.data[0]['email']
                
        # Use the specific shelter_id submitted
        shelter_id = data.get('shelter_id')
        
        if not shelter_id:
            return jsonify({"error": "Shelter selection is required"}), 400
                
        skills = data.get('role', 'General Volunteer')
        
        insert_data = {
            'shelter_id': shelter_id,
            'animal_experience': '',
            'motivation_message': data.get('message', ''),
            'status': 'PENDING',
            'skills': skills
        }
        
        if user_id:
            insert_data['user_id'] = user_id
            
        result = supabase.table('volunteers').insert(insert_data).execute()
        
        return jsonify({
            "message": "Volunteer application submitted successfully!",
            "token": "dummy-token",
            "role": "USER",
            "user": {
                "id": user_id,
                "name": full_name,
                "full_name": full_name,
                "email": email
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/shelter/volunteers', methods=['GET'])
def get_volunteers():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        shelter_id = request.args.get('shelter_id')
        
        query = supabase.table('volunteers').select('id, skills, status, motivation_message, users(full_name, email)')
        if shelter_id:
            query = query.eq('shelter_id', shelter_id)
            
        response = query.execute()
        
        formatted_vols = []
        for vol in response.data:
            applicant_name = vol.get('users', {}).get('full_name', 'Unknown Applicant') if vol.get('users') else 'Unknown Applicant'
            email = vol.get('users', {}).get('email', '') if vol.get('users') else ''
            
            formatted_vols.append({
                "id": vol['id'],
                "applicant_name": applicant_name,
                "email": email,
                "role": vol['skills'] or 'General Volunteer',
                "status": vol['status'],
                "message": vol['motivation_message']
            })
            
        return jsonify({"volunteers": formatted_vols}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/shelter/volunteer-status/<string:id>', methods=['PUT'])
def update_volunteer_status(id):
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        data = request.json
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({"error": "Status is required"}), 400
            
        response = supabase.table('volunteers').update({'status': new_status}).eq('id', id).execute()
        if not response.data:
            return jsonify({"error": "Volunteer not found"}), 404
            
        print(f"\n[MOCK EMAIL] To: Volunteer Applicant (User ID: {response.data[0].get('user_id', 'Unknown')})")
        print(f"Subject: Your PawsConnect Volunteer Application Status")
        print(f"Body: Hello! Your volunteer application has been updated to: {new_status}")
        print("--------------------------------------------------\n")
            
        return jsonify({"message": f"Volunteer status updated to {new_status}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/volunteers', methods=['GET'])
def get_user_volunteers():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        user_id = request.args.get('user_id')
        if not user_id:
             return jsonify({"error": "user_id is required"}), 400
             
        query = supabase.table('volunteers').select('id, status, motivation_message, shelters(name)').eq('user_id', user_id)
        response = query.execute()
        
        formatted_requests = []
        for req in response.data:
            shelter_name = req.get('shelters', {}).get('name', 'Unknown Shelter') if req.get('shelters') else 'Unknown Shelter'
            
            formatted_requests.append({
                "id": req['id'],
                "shelter_name": shelter_name,
                "status": req['status'],
                "message": req['motivation_message']
            })
            
        return jsonify({"requests": formatted_requests}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== 7. SUPER ADMIN ==========
@app.route('/admin/shelters', methods=['GET'])
def get_shelters():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        response = supabase.table('shelters').select('*, users(email)').execute()
        
        formatted_shelters = []
        for s in response.data:
            formatted_shelters.append({
                "id": s['id'],
                "name": s['name'],
                "email": s.get('users', {}).get('email', '') if s.get('users') else '',
                "status": "APPROVED" if s['is_approved'] else "PENDING",
                "funds": s['funds_allocated'],
                "phone": s.get('phone', ''),
                "address": s.get('address', ''),
                "description": s.get('description', '')
            })
            
        return jsonify({"shelters": formatted_shelters}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/shelters/<string:id>', methods=['PUT'])
def update_shelter_admin(id):
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        data = request.json
        update_data = {}
        if 'status' in data:
            update_data['is_approved'] = (data['status'].lower() == 'approved')
            
        if update_data:
            response = supabase.table('shelters').update(update_data).eq('id', id).execute()
            if not response.data:
                return jsonify({"error": "Shelter not found"}), 404
                
        return jsonify({"message": "Shelter status updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/donations', methods=['GET'])
def get_all_donations():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        response = supabase.table('donations').select('*').order('date', desc=True).execute()
        
        formatted_donations = []
        for d in response.data:
            formatted_donations.append({
                "id": d['id'],
                "donor": d['donor_name'] or "Anonymous",
                "amount": d['amount'],
                "date": d['date'].split('T')[0] if 'T' in d['date'] else d['date']
            })
            
        return jsonify({"donations": formatted_donations}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/allocate-funds', methods=['POST'])
def allocate_funds():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        shelter_id = data.get('shelter_id')
        
        if not shelter_id:
            return jsonify({"error": "Shelter ID is required"}), 400
            
        # Get current funds
        shelter = supabase.table('shelters').select('funds_allocated, name').eq('id', shelter_id).execute()
        if not shelter.data:
            return jsonify({"error": "Shelter not found"}), 404
            
        current_funds = float(shelter.data[0]['funds_allocated'] or 0)
        new_funds = current_funds + amount
        
        # Update funds
        supabase.table('shelters').update({'funds_allocated': new_funds}).eq('id', shelter_id).execute()
        
        return jsonify({"message": f"Successfully allocated ${amount} to {shelter.data[0]['name']}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/analytics', methods=['GET'])
def get_analytics():
    if not supabase:
        return jsonify({"error": "Database not configured"}), 500
    try:
        # Sum donations
        donations = supabase.table('donations').select('amount').eq('status', 'COMPLETED').execute()
        total_donations = sum(d['amount'] for d in donations.data) if donations.data else 0
        
        # Count shelters
        shelters_response = supabase.table('shelters').select('id', count='exact').execute()
        total_shelters = shelters_response.count if hasattr(shelters_response, 'count') else sum(1 for _ in shelters_response.data)
        
        # Count users
        users_response = supabase.table('users').select('id', count='exact').execute()
        total_users = users_response.count if hasattr(users_response, 'count') else sum(1 for _ in users_response.data)
        
        # Count pets
        pets_response = supabase.table('pets').select('id', count='exact').execute()
        total_pets = pets_response.count if hasattr(pets_response, 'count') else sum(1 for _ in pets_response.data)
        
        return jsonify({
            "total_donations": float(total_donations),
            "total_shelters": total_shelters,
            "total_users": total_users,
            "total_pets": total_pets
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/messages/user', methods=['POST'])
def save_user_message():
    if not supabase: return jsonify({"error": "No DB"}), 500
    try:
        data = request.json
        supabase.table('messages').insert({
            'sender': data.get('sender', 'User'),
            'sender_id': 'USER-' + str(random.randint(1000,9999)),
            'message': data.get('message', ''),
            'receiver_id': 'SHELTER-ID'
        }).execute()
        return jsonify({"message": "Sent"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== 7. ADMIN ENDPOINTS ==========
@app.route('/admin/shelters', methods=['GET'])
def get_admin_shelters():
    if not supabase: return jsonify({"error": "No DB"}), 500
    try:
        response = supabase.table('shelters').select('*, users(email)').execute()
        # Merge email from users table
        formatted_shelters = []
        for s in response.data:
            user_data = s.get('users', {})
            email = user_data.get('email', 'Unknown Email') if user_data else 'Unknown Email'
            formatted_shelters.append({
                "id": s['id'],
                "name": s['name'],
                "email": email,
                "phone": s['phone'],
                "address": s['address'],
                "description": s['description'],
                "status": s.get('status', 'PENDING'),
                "funds": s.get('funds', 0)
            })
        return jsonify({"shelters": formatted_shelters}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/shelters/<int:shelter_id>', methods=['PUT'])
def update_admin_shelter(shelter_id):
    if not supabase: return jsonify({"error": "No DB"}), 500
    try:
        data = request.json
        new_status = data.get('status')
        if not new_status: return jsonify({"error": "Status required"}), 400
        
        is_approved = True if new_status == 'APPROVED' else False
        
        supabase.table('shelters').update({
            'status': new_status,
            'is_approved': is_approved
        }).eq('id', shelter_id).execute()
        
        return jsonify({"message": f"Shelter {new_status.lower()} successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========== 10. PAWPAL AI CHATBOT SYSTEM ==========
MOCK_MESSAGES = []

@app.route('/api/public-shelters', methods=['GET'])
def public_shelters():
    # Return a mock list of shelters for the sidebar when a User views the page
    return jsonify([
        {"id": "shelter1", "shelter_name": "Furry Friends Shelter"},
        {"id": "shelter2", "shelter_name": "Happy Paws Rescue"},
        {"id": "shelter3", "shelter_name": "Paradise Animal Centre"}
    ]), 200

@app.route('/api/shelter-conversations', methods=['GET'])
def shelter_conversations():
    # Helper to find distinct users that the shelter has chatted with
    shelter_id = "shelter1" 
    
    user_ids = set()
    for m in MOCK_MESSAGES:
        if str(m['shelter_id']) == shelter_id:
            user_ids.add(str(m['user_id']))
            
    return jsonify([{"id": uid, "name": "User " + uid} for uid in user_ids]), 200

@app.route('/api/send-message', methods=['POST'])
def api_send_message():
    data = request.json
    
    user_id = data.get("user_id")
    shelter_id = data.get("shelter_id")
    content = data.get("content")
    sender_type = data.get("sender_type", "user") 
    
    # 1. Save the Incoming Message
    new_msg = {
        "id": str(len(MOCK_MESSAGES) + 1),
        "user_id": user_id,
        "shelter_id": shelter_id,
        "sender_type": sender_type,
        "content": content,
        "created_at": datetime.utcnow().isoformat()
    }
    MOCK_MESSAGES.append(new_msg)
    
    # 2. Automated AI Reply (Only fires when a REGULAR USER sends a text)
    if sender_type == "user":
        lower_content = content.lower()
        
        # Default fallback response
        ai_reply = f"Hi! I am the AI Assistant. I received your message: '{content}'. How can I help you today?"
        
        # Keyword matching logic
        if any(greeting in lower_content for greeting in ["hello", "hi ", "hey "]) or lower_content in ["hi", "hey", "hello"]:
            ai_reply = "Hello there! Welcome! How can we assist you today?"
        elif "cat" in lower_content or "kitten" in lower_content:
            ai_reply = "We always have wonderful cats looking for loving homes! Please check out the 'Adopt a Pet' section."
        elif "dog" in lower_content or "puppy" in lower_content:
            ai_reply = "We have many fantastic dogs and puppies waiting for a family! Head over to the 'Adopt a Pet' section to meet them."
        elif "adopt" in lower_content:
            ai_reply = "To adopt, simply find a pet you love and click 'Request Adoption' on their detail page! We'll review your application within 24-48 hours."
        elif "ok" == lower_content.strip() or "okay" in lower_content or "thanks" in lower_content or "thank you" in lower_content:
            ai_reply = "You're very welcome! Let me know if you need anything else."

        # Save the AI's Message
        bot_msg = {
            "id": str(len(MOCK_MESSAGES) + 2),
            "user_id": user_id,
            "shelter_id": shelter_id,
            "sender_type": "shelter", # Pretend the AI is the shelter admin responding
            "content": ai_reply,
            "created_at": datetime.utcnow().isoformat()
        }
        MOCK_MESSAGES.append(bot_msg)
        
    return jsonify(new_msg), 201

# Endpoint to fetch chat history
@app.route('/api/messages/<user_id>/<shelter_id>', methods=['GET'])
def api_get_messages(user_id, shelter_id):
    messages = [m for m in MOCK_MESSAGES if str(m['user_id']) == str(user_id) and str(m['shelter_id']) == str(shelter_id)]
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)
