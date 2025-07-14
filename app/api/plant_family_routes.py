from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.plant_family import PlantFamily, PlantFamilyCreate
from app.services.plant_family_service import PlantFamilyService
from app.dependencies import get_plant_family_service

router = APIRouter(prefix="/plants", tags=["plants"])


@router.get("/families", response_model=List[PlantFamily])
async def get_all_plant_families(
    plant_family_service: PlantFamilyService = Depends(get_plant_family_service),
) -> List[PlantFamily]:
    """Get all plant families"""
    try:
        return await plant_family_service.get_all_plant_families()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/families", response_model=PlantFamily)
async def create_plant_family(
    plant_family_data: PlantFamilyCreate,
    plant_family_service: PlantFamilyService = Depends(get_plant_family_service),
) -> PlantFamily:
    """Create a new plant family"""
    try:
        return await plant_family_service.create_plant_family(plant_family_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/families/{plant_family_id}")
async def delete_plant_family(
    plant_family_id: str,
    plant_family_service: PlantFamilyService = Depends(get_plant_family_service),
) -> dict:
    """Delete a plant family"""
    try:
        success = await plant_family_service.delete_plant_family(plant_family_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Plant family with ID {plant_family_id} not found",
            )
        return {"message": f"Plant family {plant_family_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
