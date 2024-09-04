import os
import sys
import time
from pymongo import MongoClient

class CensusException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = CensusException.prepare_error_message(error_message, error_detail)
        self.log_error_to_mongodb(error_detail)

    @staticmethod
    def prepare_error_message(error_message: Exception, error_detail: sys) -> str:
        _, _, exc_tb = error_detail.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line_no = exc_tb.tb_lineno
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user = os.getlogin()

        error_message = (f"Error occurred script name [{filename}] at line number [{line_no}], "
                         f"error message is [{error_message}], time [{timestamp}], user [{user}]")
        return error_message

    def log_error_to_mongodb(self, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line_no = exc_tb.tb_lineno
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user = os.getlogin()

        client = MongoClient("mongodb://localhost:27017/")
        db = client["error_logs"]
        collection = db["census_exceptions"]
        log_record = {
            "timestamp": timestamp,
            "user": user,
            "location": f"{filename}:{line_no}",
            "error_message": self.error_message
        }
        collection.insert_one(log_record)

    def __repr__(self):
        return self.error_message

    def __str__(self):
        return self.error_message