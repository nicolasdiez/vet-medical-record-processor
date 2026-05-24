## BACKEND ##

# Activate backend virtual environment
```bash
cd src/backend
source venv/Scripts/activate
```

# Run backend server FastAPI (with auto-reload)
```bash
cd src/backend/
uvicorn app.main:app --reload
```

# FastAPI OpenAPI spec (swagger) and DTOs
http://localhost:8000/docs

# FastAPI health check
http://localhost:8000/health

# Run backend unit tests
```bash
cd src/backend/
PYTHONPATH=. pytest tests/ -v
```

# Run backend end2end tests
```bash
cd src/backend/
pytest tests/e2e/test_api.py -v
```

## FRONTEND ##

# Run frontend server Vite
```bash
cd src/frontend/
npm run dev
```

# WebApp in localhost
http://localhost:5173