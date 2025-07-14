from app.database.base.plant_family import PlantFamilyRepository
from mongoengine import Document, StringField, IntField

from app.models.plant_family import PlantFamilyCreate
from app.models.plant_family import PlantFamily as PlantFamilyModel


class PlantFamily(Document):
    name = StringField(required=True)
    nutrition_requirements = StringField()
    rotation_time = IntField()  # years

    meta = {
        "collection": "plant_families",
    }

    def __str__(self):
        return self.name
    

class MongoPlantFamilyRepository(PlantFamilyRepository):

    def add_plant_family(self, plant_family_create: PlantFamilyCreate) -> PlantFamilyModel:
        mongo_doc = PlantFamily(**plant_family_create.model_dump()).save()
        return PlantFamilyModel.model_validate(mongo_doc)
    
    def _get_plant_family_by_id(self, plant_family_id: str) -> PlantFamily:
        mongo_doc = PlantFamily.objects(id=plant_family_id).first()
        return mongo_doc
    
    def get_plant_family_by_id(self, plant_family_id: str) -> PlantFamilyModel:
        mongo_doc = self._get_plant_family_by_id(plant_family_id)
        return PlantFamilyModel.model_validate(mongo_doc)
    
    def delete_plant_family(self, plant_family_id: str) -> bool:
        mongo_doc = self._get_plant_family_by_id(plant_family_id)
        if mongo_doc:
            mongo_doc.delete()
            return True
        return False