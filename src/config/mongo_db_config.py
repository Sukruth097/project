import pymongo
import os
import certifi
import argparse  # Add this import
from dotenv import load_dotenv  # Add this import
from src.config.constants import *
# from src.logger import Logger
# from src.exception import Exception

load_dotenv() 

ca = certifi.where()

class MongodbClient:
    mongodb_client = None  # Renamed from client

    def __init__(self, database_name=DATABASE_NAME, collection_name=LOGS_COLLECTION_NAME) -> None:
        if MongodbClient.mongodb_client is None:  # Renamed from client
            mongo_db_url = os.getenv("MONGODB_URL")
            # print(mongo_db_url)            
            if mongo_db_url is None:
                raise Exception(f"Environment key: {mongo_db_url} is not set.")
            MongodbClient.mongodb_client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)  # Renamed from client
        self.mongodb_client = MongodbClient.mongodb_client  # Renamed from client
        self.database = self.mongodb_client[database_name]  # Renamed from client
        self.database_name = database_name
        self.collection_name = collection_name

    def create_database_and_collection(self, database_name, collection_name):
        self.database = self.client[database_name]
        self.collection_name = collection_name
        self.database.create_collection(collection_name)

    def list_databases(self):
        return self.mongodb_client.list_database_names()  
    def list_collections(self):
        return self.database.list_collection_names()  

    def set_new_mongodb_url(self, new_mongodb_url):
        MongodbClient.mongodb_client = pymongo.MongoClient(new_mongodb_url, tlsCAFile=ca)  # Renamed from client
        self.mongodb_client = MongodbClient.mongodb_client  
        self.database = self.mongodb_client[self.database_name]  

    def upload_record(self, record):
        collection = self.database[self.collection_name]
        collection.insert_one(record)

    def delete_record(self, query):
        collection = self.database[self.collection_name]
        collection.delete_one(query)

    def upload_multiple_records(self, records):
        collection = self.database[self.collection_name]
        collection.insert_many(records)  # New method to upload multiple records

    def delete_multiple_records(self, query):
        collection = self.database[self.collection_name]
        collection.delete_many(query)  # New method to delete multiple records

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MongoDB Client Configuration")
    parser.add_argument("-d", "--database", type=str,default=DATABASE_NAME, help="Database name")
    parser.add_argument("-c", "--collection", type=str, default=LOGS_COLLECTION_NAME, help="Collection name")
    parser.add_argument("-lc", "--list_collections", action="store_true", help="List all collections")
    parser.add_argument("-ld", "--list_databases", action="store_true", help="List all databases")
    args = parser.parse_args()

    # client = MongodbClient(database_name=args.database, collection_name=args.collection)
    try:
        client = MongodbClient(database_name=args.database, collection_name=args.collection)
        print("Connection to MongoDB was successful.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
    
    if args.list_databases:
        print("Databases:", client.list_databases())
    
    if args.list_collections:
        print("Collections:", client.list_collections())
    
    if args.database and args.collection:
        if args.database not in client.list_databases() or args.collection not in client.list_collections():
            client.create_database_and_collection(args.database, args.collection)