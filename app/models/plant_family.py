from app.models.base_model import BusinessModelBase


class PlantFamilyBase(BusinessModelBase):
    name: str
    nutrition_requirements: str
    rotation_time: int


class PlantFamily(PlantFamilyBase):
    id: int


class PlantFamilyCreate(PlantFamilyBase):
    pass
