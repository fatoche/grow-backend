from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.bed import Bed, BedCreate, BedCreationRequest, BedCreationResponse
from app.services.bed_service import BedService
from app.dependencies import get_bed_service

router = APIRouter(prefix="/garden", tags=["garden"])


@router.post("/beds", response_model=BedCreationResponse)
async def create_beds(
    request: BedCreationRequest, bed_service: BedService = Depends(get_bed_service)
) -> BedCreationResponse:
    """Create multiple beds with the same dimensions"""
    try:
        return await bed_service.create_beds(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/beds/with-cleanup", response_model=BedCreationResponse)
async def create_beds_with_cleanup(
    request: BedCreationRequest, bed_service: BedService = Depends(get_bed_service)
) -> BedCreationResponse:
    """Delete all existing beds and create new ones"""
    try:
        return await bed_service.create_beds_with_cleanup(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/beds/all")
async def delete_all_beds(bed_service: BedService = Depends(get_bed_service)) -> dict:
    """Delete all beds"""
    try:
        deleted_count = await bed_service.delete_all_beds()
        return {"message": f"Successfully deleted {deleted_count} beds"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/beds", response_model=List[Bed])
async def get_all_beds(bed_service: BedService = Depends(get_bed_service)) -> List[Bed]:
    """Get all beds"""
    try:
        return await bed_service.get_all_beds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/beds/{bed_id}", response_model=Bed)
async def get_bed_by_id(
    bed_id: int, bed_service: BedService = Depends(get_bed_service)
) -> Bed:
    """Get a bed by ID"""
    try:
        return await bed_service.get_bed_by_id(bed_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/beds/{bed_id}", response_model=Bed)
async def update_bed(
    bed_id: int, bed_data: BedCreate, bed_service: BedService = Depends(get_bed_service)
) -> Bed:
    """Update a bed"""
    try:
        return await bed_service.update_bed(bed_id, bed_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/beds/{bed_id}")
async def delete_bed(
    bed_id: int, bed_service: BedService = Depends(get_bed_service)
) -> dict:
    """Delete a bed"""
    try:
        success = await bed_service.delete_bed(bed_id)
        if not success:
            raise HTTPException(
                status_code=404, detail=f"Bed with ID {bed_id} not found"
            )
        return {"message": f"Bed {bed_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
