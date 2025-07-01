import uuid
from typing import List, Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from app.database.base import BedRepository
from app.models.bed import Bed, BedCreate


class MongoBedRepository(BedRepository):
    """MongoDB implementation of BedRepository"""

    def __init__(self, mongo_uri: str, database_name: str = "grow"):
        self.client = MongoClient(mongo_uri)
        self.db: Database = self.client[database_name]
        self.collection: Collection = self.db["beds"]

    def _generate_id(self) -> str:
        """Generate a unique ID for a bed"""
        return f"bed_{uuid.uuid4().hex[:8]}"

    def _document_to_bed(self, doc: dict) -> Bed:
        """Convert MongoDB document to Bed model"""
        return Bed(
            id=doc["_id"],
            length=doc["length"],
            width=doc["width"],
            plant_families=doc.get("plant_families", []),
        )

    def _bed_to_document(self, bed: BedCreate) -> dict:
        """Convert BedCreate model to MongoDB document"""
        return {
            "_id": self._generate_id(),
            "length": bed.length,
            "width": bed.width,
            "plant_families": [],
        }

    async def create_bed(self, bed: BedCreate) -> Bed:
        """Create a single bed in MongoDB"""
        document = self._bed_to_document(bed)
        result = self.collection.insert_one(document)
        return self._document_to_bed(document)

    async def create_multiple_beds(self, beds: List[BedCreate]) -> List[Bed]:
        """Create multiple beds in MongoDB"""
        documents = [self._bed_to_document(bed) for bed in beds]
        result = self.collection.insert_many(documents)
        return [self._document_to_bed(doc) for doc in documents]

    async def get_bed_by_id(self, bed_id: str) -> Optional[Bed]:
        """Get a bed by its ID from MongoDB"""
        document = self.collection.find_one({"_id": bed_id})
        if document:
            return self._document_to_bed(document)
        return None

    async def get_all_beds(self) -> List[Bed]:
        """Get all beds from MongoDB"""
        documents = self.collection.find()
        return [self._document_to_bed(doc) for doc in documents]

    async def update_bed(self, bed_id: str, bed: BedCreate) -> Optional[Bed]:
        """Update a bed in MongoDB"""
        update_data = {"length": bed.length, "width": bed.width}
        result = self.collection.update_one({"_id": bed_id}, {"$set": update_data})
        if result.modified_count > 0:
            return await self.get_bed_by_id(bed_id)
        return None

    async def delete_bed(self, bed_id: str) -> bool:
        """Delete a bed from MongoDB"""
        result = self.collection.delete_one({"_id": bed_id})
        return result.deleted_count > 0

    def close(self):
        """Close the MongoDB connection"""
        self.client.close()
