
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

class MongoDBHandler:
    def __init__(self):
        self.uri = os.getenv('MONGODB_URI')
        self.client = None
        self.db = None
        
    def connect(self, database_name="topworldtrending"):
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.db = self.client[database_name]
            self.client.admin.command('ping')
            print("✅ Connected to MongoDB successfully!")
            return True
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            return False
            
    def save_products(self, products, collection_name):
        if not self.db:
            self.connect()
        try:
            collection = self.db[collection_name]
            result = collection.insert_many(products)
            return len(result.inserted_ids)
        except Exception as e:
            print(f"❌ Error saving to MongoDB: {e}")
            return 0
            
    def close(self):
        if self.client:
            self.client.close()
