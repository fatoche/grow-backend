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
            index=doc["index"],
            length=doc["length"],
            width=doc["width"],
            plant_families=doc.get("plant_families", []),
        )

    def _bed_to_document(self, bed: BedCreate, index: int) -> dict:
        """Convert BedCreate model to MongoDB document"""
        return {
            "_id": self._generate_id(),
            "index": index,
            "length": bed.length,
            "width": bed.width,
            "plant_families": [],
        }

    async def create_bed(self, bed: BedCreate) -> Bed:
        """Create a single bed in MongoDB"""
        # Get the next available index
        max_index = await self._get_max_index()
        index = max_index + 1

        document = self._bed_to_document(bed, index)
        result = self.collection.insert_one(document)
        return self._document_to_bed(document)

    async def create_multiple_beds(self, beds: List[BedCreate]) -> List[Bed]:
        """Create multiple beds in MongoDB"""
        # Since this is called after delete_all_beds, we start from index 1
        documents = []
        for i, bed in enumerate(beds):
            index = i + 1
            documents.append(self._bed_to_document(bed, index))

        result = self.collection.insert_many(documents)
        return [self._document_to_bed(doc) for doc in documents]

    async def _get_max_index(self) -> int:
        """Get the maximum index currently in the database"""
        result = self.collection.find_one(sort=[("index", -1)])
        return result["index"] if result else 0

    async def get_bed_by_id(self, bed_id: str) -> Optional[Bed]:
        """Get a bed by its ID from MongoDB"""
        document = self.collection.find_one({"_id": bed_id})
        if document:
            return self._document_to_bed(document)
        return None

    async def get_all_beds(self) -> List[Bed]:
        """Get all beds from MongoDB"""
        documents = self.collection.find().sort("index", 1)
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

    async def delete_all_beds(self) -> int:
        """Delete all beds from MongoDB"""
        result = self.collection.delete_many({})
        return result.deleted_count

    def close(self):
        """Close the MongoDB connection"""
        self.client.close()
