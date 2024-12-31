from src.utils.data_helper.pdfhelper import PDFFileHandler
from src.utils import log_execution_time
from src.logger import logger
from src.exception import PocException
# from typing import List
from src.config.constants import *
from src.entity.config_entity import DataTransformationConfig
# from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from src.utils.data_helper import file_type_acceptance_list
from src.utils import write_json_file
import mlflow
import dagshub
import os
import sys
import asyncio
import time

file_type_count = {file_type: 0 for file_type in file_type_acceptance_list()}
file_type_count["rejected_files_count"] = 0
rejected_files = []

dagshub.init(repo_owner='sukruthav007', repo_name='project', mlflow=True)
mlflow.set_experiment("LLM-Education-POC")

class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig): #, data_ingestion_artifact: DataIngestionArtifact):
        self.data_transformation_config = data_transformation_config
        # self.data_ingestion_artifact = data_ingestion_artifact
        self.mlflow_run = mlflow.start_run(run_name="Data Transformation")

    @log_execution_time
    def validate_file_type(self, file_type, data_dir):
        try:
            logger.info("Starting file type validation.")
            metadata = {
                "Context": "Metadata of Data Transformation component which contains the accepted and rejected data files list",
                "timestamp": time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()),
                "user_info": USERNAME
            }
            
            for file in os.listdir(data_dir):
                type = file.split(".")[-1]
                if type in file_type:
                    file_type_count[type] += 1
                else:
                    logger.info(f"Removing file: {os.path.join(data_dir, file)}")
                    file_path = os.path.join(data_dir, file)
                    os.remove(file_path)
                    file_type_count["rejected_files_count"] += 1
                    rejected_files.append(file)
            
            metadata.update({
                'filenames': os.listdir(data_dir),
                'file_type_count': file_type_count,
                'rejected_files': rejected_files
            })
            write_json_file(self.data_transformation_config.metadata_filename, metadata)
            
            mlflow.log_params(file_type_count)
            mlflow.log_artifact(self.data_transformation_config.metadata_filename)
            
            logger.info("File type validation completed successfully.")
            return data_dir
        except Exception as e:
            logger.error(f"Error during file type validation: {e}")
            raise PocException(e, sys)
    
    @log_execution_time
    async def pdf_file_handler(self, pdf_dir):
        try:
            logger.info("Starting PDF file handling.")
            accepted_files_type = file_type_acceptance_list()
            mlflow.log_param("pdf_dir", pdf_dir)
            files = self.validate_file_type(accepted_files_type, pdf_dir)
            pdf_handler = PDFFileHandler(files)
            text, image, table = await pdf_handler.run_pdf_processing()  
            # mlflow.log_artifact(text[0])
            # mlflow.log_artifact(image[0])
            # mlflow.log_artifact(table[0])

            logger.info("PDF file handling completed successfully.")
            return text, image, table
        except Exception as e:
            logger.error(f"Error during PDF file handling: {e}")
            raise PocException(e, sys)
        finally:
            mlflow.end_run()

if __name__ == "__main__":
    dtc = DataTransformationConfig()
    # dia = None
    dtcomp = DataTransformation(dtc)
    path = os.path.join(os.getcwd(), "artifacts/12_31_2024_16_29_34/DataIngestion/rawdata/cracked-output")
    
    loop = asyncio.get_event_loop()
    text, image, table=loop.run_until_complete(dtcomp.pdf_file_handler(path))
    print(text[0])
    # print(f"----->{path}")
    # print(f"------>{os.listdir(path)}")
    # type = file_type_acceptance_list()
    # files = dtcomp.validate_file_type(type, path)
    # print(f"after removal----->{os.listdir(path)}")
