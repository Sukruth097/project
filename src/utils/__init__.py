import time
from src.logger import logger
from src.exception import PocException
import yaml
import json
import sys
import os
from typing import List
import shutil

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        logger.info(f"Execution time for {func.__name__}: {int(minutes)} min {seconds:.3f} sec")
        return result
    return wrapper

def write_yaml_file(file_path: str, data: dict = None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as yaml_file:
            if data is not None:
                yaml.dump(data, yaml_file)
    except Exception as e:
        raise PocException(e, sys)


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise PocException(e, sys)




# def create_directories(directories_list: List[str], new_directory=False):
#     try:

#         for dir_path in directories_list:
#             if dir_path.startswith("s3"):
#                 continue
#             if os.path.exists(dir_path) and new_directory:
#                 shutil.rmtree(dir_path)
#                 logger.info(f"Directory removed: {dir_path}")
#             os.makedirs(dir_path, exist_ok=True)
#             logger.info(f"Directory created: {dir_path}")
#     except Exception as e:
#         raise PocException(e, sys)