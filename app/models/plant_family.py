from app.models.base_model import BusinessModelBase


class PlantFamilyBase(BusinessModelBase):
    name: str
    nutrition_requirements: str
    rotation_time: int


class PlantFamily(PlantFamilyBase):
    id: str


class PlantFamilyCreate(PlantFamilyBase):
    pass
