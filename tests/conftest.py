"""Shared test fixtures for all tests"""
import os
import pytest
import logging
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import ProgrammingError

from main import app
from app.database.sql.models import Base

# Set up logging
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Get test database URL from environment or use default"""
    return os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://grow_user:grow_password@localhost:5434/grow_test_db"
    )


@pytest.fixture(scope="session")
async def setup_test_database(test_database_url: str):
    """Create the test database if it doesn't exist (runs once per session)"""
    # Parse the test database URL to get connection info
    parts = test_database_url.split("/")
    db_name = parts[-1]
    base_url = "/".join(parts[:-1]) + "/postgres"  # Connect to default postgres db
    
    # Convert to async URL
    async_base_url = base_url.replace("postgresql://", "postgresql+asyncpg://")
    
    # Create engine connected to postgres database
    engine = create_async_engine(async_base_url, echo=False, isolation_level="AUTOCOMMIT")
    
    try:
        async with engine.connect() as conn:
            # Check if database exists
            result = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            )
            exists = result.scalar() is not None
            
            if not exists:
                # Create the test database
                await conn.execute(text(f"CREATE DATABASE {db_name}"))
                logger.info(f"Created test database: {db_name}")
            else:
                logger.info(f"Test database already exists: {db_name}")
    finally:
        await engine.dispose()
    
    yield
    
    # Optional: Drop the test database after all tests
    # Uncomment if you want to clean up the database after the test session
    # async with engine.connect() as conn:
    #     await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))


@pytest.fixture(scope="function")
async def clean_database(test_database_url: str, setup_test_database) -> Generator:
    """
    Clean database fixture that creates tables before each test
    and drops them after
    """
    # Convert to async URL
    async_url = test_database_url.replace("postgresql://", "postgresql+asyncpg://")
    
    # Create engine
    engine = create_async_engine(async_url, echo=False)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
def client() -> Generator:
    """FastAPI TestClient for making HTTP requests"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def override_database_url(test_database_url: str, monkeypatch):
    """Override the database URL for tests"""
    monkeypatch.setenv("DATABASE_URL", test_database_url)
