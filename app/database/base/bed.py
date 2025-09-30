from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.bed import Bed, BedCreate


class BedRepository(ABC):
    """Abstract base class for bed database operations"""

    @abstractmethod
    async def create_bed(self, bed: BedCreate) -> Bed:
        """Create a single bed in the database"""
        pass

    @abstractmethod
    async def create_multiple_beds(self, beds: List[BedCreate]) -> List[Bed]:
        """Create multiple beds in the database"""
        pass

    @abstractmethod
    async def get_bed_by_id(self, bed_id: int) -> Optional[Bed]:
        """Get a bed by its ID"""
        pass

    @abstractmethod
    async def get_all_beds(self) -> List[Bed]:
        """Get all beds from the database"""
        pass

    @abstractmethod
    async def update_bed(self, bed_id: int, bed: BedCreate) -> Optional[Bed]:
        """Update a bed in the database"""
        pass

    @abstractmethod
    async def delete_bed(self, bed_id: int) -> bool:
        """Delete a bed from the database"""
        pass

    @abstractmethod
    async def delete_all_beds(self) -> int:
        """Delete all beds from the database and return the number of deleted beds"""
        pass
