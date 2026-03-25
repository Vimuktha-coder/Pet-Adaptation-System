# Deployment Instructions

## Backend (Flask, Python)
1. Hosted on a platform like Render or Heroku.
2. Initialize environment: `pip install -r requirements.txt`
3. Add Environment Variables (`SUPABASE_URL`, `SUPABASE_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`) to your hosting provider settings.
4. Run: `gunicorn app:app` (Make sure to install gunicorn `pip install gunicorn`)

## Frontend (HTML, CSS, JS)
1. Deploy to Vercel, Netlify, or GitHub Pages.
2. Link the frontend API calls to your deployed Flask Backend URL in `js/main.js`.

## Database (Supabase)
1. Go to Supabase dashboard and run the `database/schema.sql` via the SQL Editor to initialize the tables.
