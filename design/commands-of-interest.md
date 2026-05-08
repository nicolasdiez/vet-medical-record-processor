# Activate virtual environment
cd src/backend
source venv/Scripts/activate

# Start the FastAPI server with auto-reload
uvicorn app.main:app --reload

# FastAPI OpenAPI spec (swagger) and DTOs
http://localhost:8000/docs

#