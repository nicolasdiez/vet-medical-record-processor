# BACKEND

## Activate backend virtual environment
```bash
cd src/backend
source venv/Scripts/activate
```

## Run backend server FastAPI (with auto-reload)
```bash
cd src/backend/
uvicorn app.main:app --reload
```

## FastAPI OpenAPI spec (swagger) and DTOs
http://localhost:8000/docs

## FastAPI health check
http://localhost:8000/health

## Run all backend tests (unit + end2end)
```bash
cd src/backend/
PYTHONPATH=. pytest tests/ -v
```

## Run backend unit tests
```bash
cd src/backend/
PYTHONPATH=. pytest tests/unit/ -v
```

## Run backend end2end tests
```bash
cd src/backend/
PYTHONPATH=. pytest tests/e2e/ -v
```

## Run backend static analysis and code hygiene (Ruff)
```bash
cd src/backend/
# Checks for style (PEP 8) and logic errors using the custom configuration from /src/backend/ruff.toml, fixing issues automatically
ruff check . --fix
```

## Run backend static type checking (Mypy)
```bash
cd src/backend/
# Strictly verifies that all functions, ports, and use cases comply with explicit type hints using CLI flags
mypy app/ --disallow-untyped-defs
```


# FRONTEND

## Run frontend server Vite
```bash
cd src/frontend/
npm run dev
```

## WebApp in localhost
http://localhost:5173