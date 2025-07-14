import os
from functools import lru_cache
from app.database.mongo.bed import MongoBedRepository
from app.database.mongo.plant_family import MongoPlantFamilyRepository
from app.services.bed_service import BedService
from app.services.plant_family_service import PlantFamilyService


@lru_cache()
def get_mongo_uri() -> str:
    """Get MongoDB URI from environment variables"""
    return os.getenv("MONGO_URI", "")


def get_bed_repository() -> MongoBedRepository:
    """Get bed repository instance"""
    mongo_uri = get_mongo_uri()
    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")
    return MongoBedRepository(mongo_uri)


def get_bed_service() -> BedService:
    """Get bed service instance"""
    repository = get_bed_repository()
    return BedService(repository)


def get_plant_family_repository() -> MongoPlantFamilyRepository:
    """Get plant family repository instance"""
    return MongoPlantFamilyRepository()


def get_plant_family_service() -> PlantFamilyService:
    """Get plant family service instance"""
    repository = get_plant_family_repository()
    return PlantFamilyService(repository)
