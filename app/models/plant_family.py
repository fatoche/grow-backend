from typing import Any
from pydantic import BaseModel


class PlantFamilyBase(BaseModel):
    name: str
    nutrition_requirements: str
    rotation_time: int


class PlantFamily(PlantFamilyBase):
    id: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj: Any, **kwargs) -> "PlantFamily":
        obj.id = str(obj.id)
        return super().model_validate(obj, **kwargs)


class PlantFamilyCreate(PlantFamilyBase):
    pass