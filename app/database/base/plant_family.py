from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.plant_family import PlantFamily, PlantFamilyCreate


class PlantFamilyRepository(ABC):
    @abstractmethod
    async def create_plant_family(self, plant_family: PlantFamilyCreate) -> PlantFamily:
        """Create a new plant family"""
        pass

    @abstractmethod
    async def get_plant_family_by_id(
        self, plant_family_id: int
    ) -> Optional[PlantFamily]:
        """Get a plant family by its ID"""
        pass

    @abstractmethod
    async def get_all_plant_families(self) -> List[PlantFamily]:
        """Get all plant families"""
        pass

    @abstractmethod
    async def delete_plant_family(self, plant_family_id: int) -> bool:
        """Delete a plant family"""
        pass
