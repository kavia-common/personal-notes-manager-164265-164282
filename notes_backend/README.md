# Notes Backend

Flask-based backend providing RESTful APIs for authentication and CRUD operations on Notes.

## Features
- Register and login with JWT-based auth.
- Create, list (paginated), get, update, and delete notes.
- OpenAPI docs via flask-smorest at /docs.
- Database integration via SQLAlchemy (use DATABASE_URL env).

## Environment variables
See .env.example for all options:
- SECRET_KEY, JWT_SECRET_KEY
- DATABASE_URL (from notes_database dependency)
- HOST, PORT, FLASK_DEBUG
- API_TITLE, API_VERSION, OPENAPI_VERSION, OPENAPI_URL_PREFIX
- CORS_ORIGINS

## Run
1. Copy .env.example to .env and fill values.
2. Install dependencies:
   pip install -r requirements.txt
3. Start:
   python run.py

## API Summary
- GET /           -> health
- POST /auth/register
- POST /auth/login
- GET /notes/?page=1&per_page=10
- POST /notes/
- GET /notes/<id>
- PUT /notes/<id>
- DELETE /notes/<id>

Authorization: Bearer <token>
