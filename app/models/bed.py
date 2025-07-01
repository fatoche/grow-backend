from pydantic import BaseModel, Field
from typing import List


class BedBase(BaseModel):
    length: int = Field(..., gt=0, description="Length of the bed in centimeters")
    width: int = Field(..., gt=0, description="Width of the bed in centimeters")


class BedCreate(BedBase):
    pass


class Bed(BedBase):
    id: str = Field(..., description="Unique identifier for the bed")
    index: int = Field(..., description="User-readable bed index (1-based)")
    plant_families: List[str] = Field(
        default_factory=list, description="List of plant families in this bed"
    )

    class Config:
        from_attributes = True


class BedCreationRequest(BaseModel):
    numberOfBeds: int = Field(..., gt=0, description="Number of beds to create")
    length: int = Field(..., gt=0, description="Length of each bed in centimeters")
    width: int = Field(..., gt=0, description="Width of each bed in centimeters")


class BedCreationResponse(BaseModel):
    beds: List[Bed]
    message: str
