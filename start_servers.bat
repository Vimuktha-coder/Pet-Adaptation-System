@echo off
echo Starting Backend Server on port 8000...
start cmd /k "cd backend && venv\Scripts\activate && python app.py"

echo Starting Frontend Server on port 8080...
start cmd /k "cd frontend && python -m http.server 8080"

echo.
echo Application started!
echo Backend API is running at http://localhost:8000
echo Frontend is accessible at http://localhost:8080 (You must use this URL for Stripe redirects to work properly)
echo.
pause
