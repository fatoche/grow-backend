from pydantic import BaseModel


class PlantFamilyBase(BaseModel):
    name: str
    nutrition_requirements: str
    rotation_time: int


class PlantFamily(PlantFamilyBase):
    id: str

    class Config:
        from_attributes = True


class PlantFamilyCreate(PlantFamilyBase):
    pass