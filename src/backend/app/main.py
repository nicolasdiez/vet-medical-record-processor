from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

# --- Config ---
from app.config import settings

# --- Routers ---
from app.infrastructure.inbound.api.routers import (
    documents_router, 
    pets_router, 
    clinical_data_router,
    # The placeholder functions than need to be overriden with injections:
    get_extract_use_case, 
    get_save_use_case, 
    get_history_use_case
)

# --- Database & Models ---
from app.infrastructure.outbound.persistence.database import engine, AsyncSessionLocal
from app.infrastructure.outbound.persistence.models import Base

# --- Adapters ---
from app.infrastructure.outbound.persistence.sql_pet_repository import SQLPetRepositoryAdapter
from app.infrastructure.outbound.persistence.sql_medical_record_repository import SQLMedicalRecordRepositoryAdapter
from app.infrastructure.outbound.gemini_medical_record_extractor import LLMGeminiMedicalRecordExtractorAdapter

# --- Use Cases ---
from app.application.use_cases.extract_clinical_data import ExtractClinicalDataUseCase
from app.application.use_cases.save_clinical_data import SaveClinicalDataUseCase
from app.application.use_cases.get_pet_clinical_history import GetPetClinicalHistoryUseCase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes the SQLite database tables on startup.
    """
    async with engine.begin() as conn:
        # In a production environment with PostgreSQL, use Alembic for migrations.
        # For this MVP with SQLite, we create tables directly on startup.
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup on shutdown
    await engine.dispose()


app = FastAPI(
    title="Vet Medical Record Processor API",
    description="API for extracting and structuring veterinary medical records.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",     # Frontend deployed in local dev env (Vite)
        "http://localhost:8080",    # Frontend deployed in pro env (Docker Nginx)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(pets_router)
app.include_router(clinical_data_router)


# ==============================================================================
# FastAPI ROUTERS DEPENDENCY INJECTION WIRING (The core of Hexagonal Architecture)
# ==============================================================================

async def get_db_session() -> AsyncSession: # type: ignore
    """Provides a fresh database session for each request."""
    async with AsyncSessionLocal() as session:
        yield session

async def build_extract_use_case(session: AsyncSession = Depends(get_db_session)) -> ExtractClinicalDataUseCase:
    pet_repo = SQLPetRepositoryAdapter(session)
    
    medical_extractor = LLMGeminiMedicalRecordExtractorAdapter(
        api_key=settings.GEMINI_API_KEY, 
        model_id=settings.GEMINI_MODEL
    )
    
    return ExtractClinicalDataUseCase(
        medical_extractor=medical_extractor,
        pet_repository=pet_repo
    )

async def build_save_use_case(session: AsyncSession = Depends(get_db_session)) -> SaveClinicalDataUseCase:
    pet_repo = SQLPetRepositoryAdapter(session)
    medical_repo = SQLMedicalRecordRepositoryAdapter(session)
    
    return SaveClinicalDataUseCase(
        pet_repository=pet_repo,
        medical_record_repository=medical_repo,
        session=session
    )

async def build_history_use_case(session: AsyncSession = Depends(get_db_session)) -> GetPetClinicalHistoryUseCase:
    medical_repo = SQLMedicalRecordRepositoryAdapter(session)
    return GetPetClinicalHistoryUseCase(medical_record_repository=medical_repo)


# Overriding the router placeholders with our actual factory functions
app.dependency_overrides[get_extract_use_case] = build_extract_use_case
app.dependency_overrides[get_save_use_case] = build_save_use_case
app.dependency_overrides[get_history_use_case] = build_history_use_case


# App health check
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "message": "Backend is running successfully!"}