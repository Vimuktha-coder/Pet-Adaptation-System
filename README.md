# 🐾 Multi-Shelter Pet Adoption Platform 🐾

Welcome to the **Multi-Shelter Pet Adoption Platform**! This is a comprehensive, full-stack application designed to connect prospective pet adopters with multiple animal shelters. It provides dedicated dashboards for different user roles (System Admins, Shelter Managers, Volunteers) and features a beautiful frontend for users to find their next cute furry friend.
---

## ✨ Key Features

- **🐾 Pet Adoption Portal:** Users can browse, filter, and view detailed profiles of pets available for adoption across multiple shelters.
- **🏢 Multi-Shelter Management:** Each shelter gets its own management dashboard to upload pet profiles, process adoption requests, and manage their staff.
- **👑 Role-Based Access Control:**
  - **Super Admin:** Manage the entire platform, oversee all shelters, and view platform-wide analytics.
  - **Shelter Manager:** Manage specific shelter operations, update pet statuses, and handle adoption applications.
  - **Volunteer:** View tasks, assist with specific pets, and coordinate with shelter managers.
  - **Adopter/User:** Browse pets, submit adoption applications, and interact with the AI chatbot.
- **💳 Integrated Donations:** Supports secure online donations powered by **Stripe**.
- **🤖 AI Chatbot Assistant:** Integrated chatbot widget to answer user queries and guide adopters.

---

## 🛠️ Technology Stack

This application is built with a decoupled architecture, separating the client and server.

### Frontend
- **HTML5 / CSS3 / Vanilla JavaScript**
- Fully responsive design tailored for mobile and desktop views.
- **Pages include:** Home, Pet Listing, Pet Details, Adoption Form, Admin/Shelter/Volunteer Dashboards, Login/Register, Donation.

### Backend
- **Python 3 / Flask:** Provides RESTful API endpoints.
- **Gunicorn:** WSGI HTTP Server for UNIX (production).
- **Stripe SDK:** For processing payments.
- **OpenAI / AI SDKs:** For Chatbot integration.

### Database
- **Supabase (PostgreSQL):** A highly scalable backend-as-a-service providing a robust PostgreSQL database.

---

## 🚀 Local Development Setup

Follow these steps to get the application running on your local machine.

### 1. Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- A [Supabase](https://supabase.com/) account
- A [Stripe](https://stripe.com/) account (for donation features)

### 2. Clone the Repository
```bash
git clone https://github.com/Vimuktha-coder/Pet-Adaptation-System.git
cd Pet-Adaptation-System
```

### 3. Database Initialization (Supabase)
1. Log in to your Supabase dashboard and create a new project.
2. Navigate to the **SQL Editor**.
3. Copy the contents of `database/schema.sql` and run the script to initialize all necessary tables and relationships.

### 4. Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend` directory and add the following keys:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key

   # Stripe Configuration
   STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   
   # Add your AI Keys if applicable
   # OPENAI_API_KEY=your_openai_api_key
   ```

### 5. Running the Application locally
You can start both the backend server and the frontend locally using the provided batch script (Windows) or manually.

**Using the script (Windows):**
Simply double-click the `start_servers.bat` file in the root directory.

**Running Manually:**
- **Backend:** 
  ```bash
  cd backend
  python app.py
  ```
  *(Server runs on http://127.0.0.1:5000)*
- **Frontend:**
  Use any local server like VS Code Live Server, or Python's built-in HTTP server:
  ```bash
  cd frontend
  python -m http.server 8000
  ```
  *(Frontend available at http://127.0.0.1:8000)*

---

## ☁️ Deployment Instructions

### Backend Deployment (Render / Heroku)
1. Connect your GitHub repository to your host (e.g., Render Web Service).
2. Set the build command: `pip install -r backend/requirements.txt`
3. Set the start command: `cd backend && gunicorn app:app`
4. Make sure to add all the Environment Variables from your `.env` file into the Hosting Provider's dashboard.

### Frontend Deployment (Vercel / Netlify / GitHub Pages)
1. Deploy the `frontend` folder to your static hosting provider.
2. **Important:** Before deploying, ensure that the API base URLs inside `frontend/js/main.js` are pointing to your deployed backend URL instead of `http://localhost:5000`.

---

## 🤝 Contributing
Contributions are always welcome! Ensure you test your code locally before opening a pull request.
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
*Made with ❤️ for animals in need of a forever home.*
