import os
import sys
import time
from src.config.mongo_db_config import MongodbClient
from src.config.constants import *
from src.logger import logger
import socket

class PocException(Exception):
    def __init__(self, error_message, error_detail):
        self.error_message = PocException.prepare_error_message(error_message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def prepare_error_message(error_message, error_detail):
        if isinstance(error_detail, tuple):
            _, _, exc_tb = error_detail
        else:
            exc_tb = error_detail.__traceback__
        return f"{error_message} - Error occurred in script: {exc_tb.tb_frame.f_code.co_filename} at line number: {exc_tb.tb_lineno}"

    def log_error_to_mongodb(self, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line_no = exc_tb.tb_lineno
        timestamp = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
        user = socket.gethostname() #os.getlogin()

        client = MongodbClient(database_name=DATABASE_NAME, collection_name=ERROR_COLLECTION_NAME)
        
        log_record = {
            "timestamp": timestamp,
            "user": user,
            "filename": f"{filename}",
            "line_number": f"{line_no}",
            "error_message": self.error_message
        }
        client.upload_record(log_record)

    def __repr__(self):
        return self.error_message

    def __str__(self):
        return self.error_message
