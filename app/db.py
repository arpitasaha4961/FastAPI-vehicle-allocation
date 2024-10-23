import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") 
print(MONGO_URI)
client = MongoClient(MONGO_URI)
db = client["vehicle_allocation"]


employees = db["employees"]
vehicles = db["vehicles"]
allocations = db["allocations"]
