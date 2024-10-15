import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')

try:
    # Create a MongoDB client
    client = MongoClient(MONGODB_URI)
    # print(MONGODB_URI)

    db = client['data-wrangler']

    #verify connection
    server_info = db.command("ping")
    print("Connected to MongoDB:", server_info)
    
except Exception as e:
    print("Failed to connect to MongoDB:", e)
