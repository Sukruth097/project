import logging
import os
from datetime import datetime
from src.config.constants import *
import re
from src.config.mongo_db_config import MongodbClient

# Custom formatter class
class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %I:%M:%S %p')

    def format(self, record):
        record.user = os.getlogin()
        return super().format(record)

# Function to get log file name
def get_log_file_name():
    return f"log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
log_dir="logs"
# Function to set up the logger
def setup_logger(name, log_dir="logs"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_name = get_log_file_name()
    log_file_path = os.path.join(log_dir, log_file_name)

    formatter = CustomFormatter(
        fmt="[%(asctime)s]: %(levelname)s -['User_Name']:%(user)s -['filepath']:%(pathname)s ['filename']:%(filename)s -['function_name']:%(funcName)s -['line_no']:%(lineno)d - %(message)s"
    )

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger

# Function to get the logger instance
def get_logger(name="POC"):
    return logging.getLogger(name)

setup_logger("POC")
logger = get_logger("POC")
# logger.info("This is an info message from another module.")
# logger.error("This is an error message from another module.")



# Connect to MongoDB
# client = MongodbClient()
# collection = client.collection_name

# # Function to parse a log line
# def parse_log_line(log_line):
#     pattern = re.compile(r"\[(.*?)\]: (\w+) -\['User_Name'\]:(.*?) -\['filepath'\]:(.*?) -\['filename'\]:(.*?) -\['function_name'\]:(.*?) -\['line_no'\]:(\d+) - (.*)")
#     match = pattern.match(log_line)
#     if match:
#         return {
#             "timestamp": match.group(1),
#             "level": match.group(2),
#             "user_name": match.group(3),
#             "filepath": match.group(4),
#             "filename": match.group(5),
#             "function_name": match.group(6),
#             "line_no": int(match.group(7)),
#             "message": match.group(8)
#         }
#     return None

# # Function to process a log file
# def process_log_file(file_path):
#     with open(file_path, 'r') as file:
#         logs = []
#         for line in file:
#             log_entry = parse_log_line(line.strip())
#             if log_entry:
#                 logs.append(log_entry)
        
#         if logs:
#             # Assuming all logs in the file have the same timestamp
#             timestamp = logs[0]['timestamp']
#             record = {
#                 "timestamp": timestamp,
#                 "logs": logs
#             }
#             # Insert or update the record in MongoDB
#             collection.update_one(
#                 {"timestamp": timestamp},
#                 {"$set": record},
#                 upsert=True
#             )

# # Example usage
# # log_file_path = 'path/to/your/logfile.log'
# log_file_name = get_log_file_name()
# log_file_path = os.path.join(log_dir, log_file_name)

# process_log_file(log_file_path)
# logger.info("This is an info message from another module.")
# logger.error("This is an error message from another module.")