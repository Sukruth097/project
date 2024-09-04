import pymongo
import os
import certifi
from src.config.constants import *

ca = certifi.where()

class MongodbClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        if MongodbClient.client is None:
            mongo_db_url = os.getenv(MONGODB_URL)
            if mongo_db_url is None:
                raise Exception(f"Environment key: {MONGODB_URL} is not set.")
            MongodbClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
        self.client = MongodbClient.client
        self.database = self.client[database_name]
        self.database_name = database_name
        self.collection_name = COLLECTION_NAME