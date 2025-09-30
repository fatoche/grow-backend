import os
from functools import lru_cache
from app.database.sql.bed_repository import SQLBedRepository
from app.database.sql.plant_family_repository import SQLPlantFamilyRepository
from app.services.bed_service import BedService
from app.services.plant_family_service import PlantFamilyService


@lru_cache()
def get_database_url() -> str:
    """Get PostgreSQL database URL from environment variables"""
    return os.getenv("DATABASE_URL", "postgresql://grow_user:grow_password@localhost:5434/grow_db")


def get_bed_repository() -> SQLBedRepository:
    """Get bed repository instance"""
    database_url = get_database_url()
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return SQLBedRepository(database_url)


def get_bed_service() -> BedService:
    """Get bed service instance"""
    repository = get_bed_repository()
    return BedService(repository)


def get_plant_family_repository() -> SQLPlantFamilyRepository:
    """Get plant family repository instance"""
    database_url = get_database_url()
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return SQLPlantFamilyRepository(database_url)


def get_plant_family_service() -> PlantFamilyService:
    """Get plant family service instance"""
    repository = get_plant_family_repository()
    return PlantFamilyService(repository)
