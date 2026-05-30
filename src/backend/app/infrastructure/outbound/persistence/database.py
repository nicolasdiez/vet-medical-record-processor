from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

"""
Database Configuration Module.

This module initializes the asynchronous SQLAlchemy engine and session factory 
using SQLite. It also exposes the declarative Base class 
that all ORM models must inherit from.

Attributes:
    DATABASE_URL (str): The connection string for the SQLite database.
    engine (AsyncEngine): The asynchronous SQLAlchemy engine.
    AsyncSessionLocal (async_sessionmaker): Factory for generating new async database sessions.
    Base (Any): The declarative base class for mapping Python classes to database tables.
"""

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