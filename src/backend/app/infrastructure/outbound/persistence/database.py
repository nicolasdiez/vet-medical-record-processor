from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# SQLite local database file (async driver)
DATABASE_URL = "sqlite+aiosqlite:///./vet_clinic.db"

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True to see the generated SQL queries in console
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for ORM models
Base = declarative_base()