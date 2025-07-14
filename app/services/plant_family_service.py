from typing import List, Optional
from app.database.base.plant_family import PlantFamilyRepository
from app.models.plant_family import PlantFamily, PlantFamilyCreate


class PlantFamilyService:
    """Service layer for plant family operations"""

    def __init__(self, plant_family_repository: PlantFamilyRepository):
        self.plant_family_repository = plant_family_repository

    async def create_plant_family(
        self, plant_family_data: PlantFamilyCreate
    ) -> PlantFamily:
        """Create a new plant family"""
        return await self.plant_family_repository.create_plant_family(plant_family_data)

    async def get_plant_family_by_id(self, plant_family_id: str) -> PlantFamily:
        """Get a plant family by ID"""
        plant_family = await self.plant_family_repository.get_plant_family_by_id(
            plant_family_id
        )
        if not plant_family:
            raise ValueError(f"Plant family with ID {plant_family_id} not found")
        return plant_family

    async def get_all_plant_families(self) -> List[PlantFamily]:
        """Get all plant families"""
        return await self.plant_family_repository.get_all_plant_families()

    async def delete_plant_family(self, plant_family_id: str) -> bool:
        """Delete a plant family"""
        return await self.plant_family_repository.delete_plant_family(plant_family_id)
