from src.utils.data_helper.pdfhelper import PDFFileHandler
from src.utils import log_execution_time
from src.logger import logger
from src.exception import PocException
from typing import List
from src.config.constants import *
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact
from src.utils.data_helper import file_type_acceptance_list
import mlflow
import dagshub
import os
import sys
import asyncio

ACCEPTANCE_FILE_TYPES = file_type_acceptance_list()
file_type_count = {file_type: 0 for file_type in ACCEPTANCE_FILE_TYPES}
file_type_count["rejected_files_count"] = 0
rejected_files = []

class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,data_ingestion_artifact:DataIngestionArtifact):

        self.data_transformation_config= data_transformation_config
        self.data_ingestion_artifact = data_ingestion_artifact

    def validate_file_type(self,file_type:List,data_dir):
        try:
            metadata = {
                "Context": "Metadata of Data Transformation component which contains the accpeted and rejected data files list",
                "timestamp": time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()),
                "user_info": USERNAME
                }
            file_type_accepted = file_type
            for file in os.listdir(data_dir):
                 if file_type in file_type_accepted:
                    file_type_count[f"{file_type}"] += 1
                 else:
                    os.remove(os.path.join(data_dir, file))
                    file_type_count["rejected_files_count"] += 1
                    rejected_files.append(file)
            metadata.update({
                'filenames': os.listdir(data_dir),
                'file_type_count': file_type_count,
                'rejected_files': rejected_files
            })
            return data_dir
        except Exception as e:
            print(e)
            raise PocException(e,sys)
        
    