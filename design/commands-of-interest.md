# Activate virtual environment
cd src/backend
source venv/Scripts/activate

# Run backend server FastAPI server (with auto-reload)
cd src/backend/
uvicorn app.main:app --reload

# FastAPI OpenAPI spec (swagger) and DTOs
http://localhost:8000/docs

# Run frontend server Vite
cd src/frontend/
npm run dev

# App in localhost
http://localhost:5173