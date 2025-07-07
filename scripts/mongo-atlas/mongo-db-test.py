import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from local.env (same as main.py)
load_dotenv("local.env")

uri = os.getenv("MONGO_URI")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

try:
    # Access the 'grow' database and 'beds' collection
    db = client["grow"]
    beds_collection = db["beds"]

    # Retrieve all documents from the 'beds' collection
    beds = beds_collection.find()

    # Print each document in the 'beds' collection
    for bed in beds:
        print(bed)
except Exception as e:
    print(f"An error occurred while accessing the 'beds' collection: {e}")
