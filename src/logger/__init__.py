import logging
from datetime import datetime
import os
import pandas as pd
from src.config.constants import *
from src.config.mongo_db_config import MongodbClient

# MongoDB configuration
mongodb_client = MongodbClient()
collection = mongodb_client.database[LOGS_COLLECTION_NAME]

class MongoDBHandler(logging.Handler):
    def __init__(self, collection):
        logging.Handler.__init__(self)
        self.collection = collection

    def emit(self, record):
        log_entry = self.format(record)
        self.collection.insert_one(log_entry)

    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow(),
            "level": record.levelname,
            "lineno": record.lineno,
            "filename": record.filename,
            "funcName": record.funcName,
            "message": record.msg,
            "user": os.getlogin()  # Get the current logged-in user
        }
        return log_entry

# Set up logging
logger = logging.getLogger("Education LLM Bot")
logger.setLevel(logging.INFO)

# Add MongoDB handler
mongo_handler = MongoDBHandler(collection)
logger.addHandler(mongo_handler)

# Example log
# logger.info("Logger initialized and connected to MongoDB")