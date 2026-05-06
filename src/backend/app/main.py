from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.inbound.api.routers import router as records_router

app = FastAPI(
    title="Vet Medical Record Processor API",
    description="API for extracting and structuring veterinary medical records.",
    version="1.0.0"
)

# Configure CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(records_router)

@app.get("/health", tags=["System"])
async def health_check():
    """
    Simple health check endpoint to verify the server is running.
    """
    return {"status": "ok", "message": "Backend is running successfully!"}