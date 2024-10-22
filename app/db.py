from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017"  # Adjust if you're using MongoDB Atlas or Docker
client = MongoClient(MONGO_URI)
db = client["vehicle_allocation"]

# Employee collection
employees = db["employees"]
vehicles = db["vehicles"]
allocations = db["allocations"]
