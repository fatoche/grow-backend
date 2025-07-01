from typing import List
from app.database.base import BedRepository
from app.models.bed import Bed, BedCreate, BedCreationRequest, BedCreationResponse


class BedService:
    """Service layer for bed operations"""

    def __init__(self, bed_repository: BedRepository):
        self.bed_repository = bed_repository

    async def create_beds(self, request: BedCreationRequest) -> BedCreationResponse:
        """Create multiple beds with the same dimensions"""
        # Create BedCreate objects for each bed
        beds_to_create = [
            BedCreate(length=request.length, width=request.width)
            for _ in range(request.numberOfBeds)
        ]

        # Create beds in database
        created_beds = await self.bed_repository.create_multiple_beds(beds_to_create)

        # Create response
        message = f"Successfully created {len(created_beds)} beds"
        return BedCreationResponse(beds=created_beds, message=message)

    async def get_all_beds(self) -> List[Bed]:
        """Get all beds"""
        return await self.bed_repository.get_all_beds()

    async def get_bed_by_id(self, bed_id: str) -> Bed:
        """Get a bed by ID"""
        bed = await self.bed_repository.get_bed_by_id(bed_id)
        if not bed:
            raise ValueError(f"Bed with ID {bed_id} not found")
        return bed

    async def update_bed(self, bed_id: str, bed_data: BedCreate) -> Bed:
        """Update a bed"""
        bed = await self.bed_repository.update_bed(bed_id, bed_data)
        if not bed:
            raise ValueError(f"Bed with ID {bed_id} not found")
        return bed

    async def delete_bed(self, bed_id: str) -> bool:
        """Delete a bed"""
        return await self.bed_repository.delete_bed(bed_id)
