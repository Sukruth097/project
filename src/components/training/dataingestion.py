from src.logger import logger
from src.exception import PocException
import os
import sys
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.utils import log_execution_time,write_json_file,read_json_file
from src.config.azure_config import AzureBlobManager
from src.config.constants import *
from PyPDF2 import PdfReader
# from PyPDF2 import PdfMerger
import time
import socket
from src.utils.data_helper import file_type_acceptance_list

ACCEPTANCE_FILE_TYPES = file_type_acceptance_list()
file_type_count = {file_type: 0 for file_type in ACCEPTANCE_FILE_TYPES}
file_type_count["rejected_files_count"] = 0
rejected_files=[]

class DataIngestion:
    
    @log_execution_time
    def __init__(self, data_ingestion_config:DataIngestionConfig,azure_blob_config:AzureBlobManager):
        logger.info("******************* DATA_INGESTION COMPONENT STARTED *******************")
        self.data_ingestion_config=data_ingestion_config
        self.azure_blob_config = azure_blob_config
        
    @log_execution_time    
    def download_azure_data(self):
        try:
            download_dir = self.data_ingestion_config.raw_data_dir
            azure_container_name = self.data_ingestion_config.azure_container_name
            azure_blob_name = self.data_ingestion_config.azure_blob_name
            user_info = socket.gethostname() #os.getlogin() 
            os.makedirs(os.path.dirname(self.data_ingestion_config.metadata_filename), exist_ok=True)
            # metadata_path=self.data_ingestion_config.metadata_filename
            if os.path.exists(self.data_ingestion_config.metadata_filename):
                existing_metadata = read_json_file(self.data_ingestion_config.metadata_filename)
                # existing_files = set(existing_metadata.get("filenames", [])).union(set(existing_metadata.get("rejected_files", [])))
                existing_files = set(existing_metadata.get("rejected_files", []))
                # print(f"------->{existing_files}")
            else:
                existing_files = set()
            
            logger.info(f"Starting downloading the files from azure container: {azure_container_name} and azure blob: {azure_blob_name}")
            raw_data_path, data_filenames = self.azure_blob_config.download_allfiles_in_blob(azure_container_name, download_dir, azure_blob_name, existing_files)
            logger.info(f"Successfully downloaded all the files and stored in {raw_data_path}")
            
            logger.info("Collecting the metadata of the files downloaded")
            metadata = {
                "Context": "Metadata of Data Ingestion component which contains the data files downloaded list",
                "timestamp": time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()),
                "container_name": azure_container_name,
                "blob_name": azure_blob_name,
                "new_downloaded_files": data_filenames,# os.listdir(raw_data_path) if len(os.listdir(raw_data_path))!=0 else "No files downloaded",
                "filenames": list(existing_files.union(data_filenames)),
                "user_info": user_info
            }
          
            metadata = write_json_file(self.data_ingestion_config.metadata_filename, metadata)
            logger.info(f"Metadata written to {self.data_ingestion_config.metadata_filename}")
            # print(raw_data_path, metadata)
            return raw_data_path, metadata
        except Exception as e:
            print(logger.error(e))
            PocException(e, sys)
        
    @log_execution_time
    def di_files_metadata(self,metadata_filename):
        try:
            file_metadata = read_json_file(metadata_filename)
            files=file_metadata.get('filenames')
            for file in files:
                file_type=file.split('.')[-1]
                if file_type in ACCEPTANCE_FILE_TYPES:
                    file_type_count[f"{file_type}"]+=1
                else:
                    file_type_count["rejected_files_count"]+=1
                    rejected_files.append(file)
                    files.remove(file)
            file_metadata.update({
                'file_type_count': file_type_count,
                'rejected_files': rejected_files
            })
            write_json_file(metadata_filename, file_metadata)
        except Exception as e:
            print(logger.error(e))
            PocException(e,sys)
    
    @log_execution_time
    def trigger_data_ingestion(self):
        try:
            azure_raw_data,azure_di_metadata = self.download_azure_data()
            self.di_files_metadata(azure_di_metadata)
            blob_raw_data = os.path.join(os.getcwd(),azure_raw_data)
            data_ingestion_artifact = DataIngestionArtifact(blob_raw_data,azure_di_metadata)
            return data_ingestion_artifact
        except Exception as e:
            print(logger.error(e))
            PocException(e,sys)
            
            
if __name__ == "__main__":
    data_ingestion_config= DataIngestionConfig()
    azure_blob_config = AzureBlobManager()
    data_ingestion_component = DataIngestion(data_ingestion_config,azure_blob_config)
    data_ingestion_artifact=data_ingestion_component.trigger_data_ingestion()
    # print(f"-------->{data_ingestion_artifact.azure_raw_data}")
    # print(data_ingestion_artifact.metadata_file_path)
    # print(f"---->{os.listdir(data_ingestion_artifact.azure_raw_data)}")

    # for file in os.listdir(data_path):
    #     if file.endswith('.pdf'):
    #         file_path = os.path.join(data_path, file)
    #         with open(file_path, 'rb') as file:
    #             pdf_reader = PdfReader(file)
    #             print(f"Number of pages in {file_path} is {len(pdf_reader.pages)}")   
    # azure_raw_data,azure_di_metadata=data_ingestion_component.download_azure_data()
    # data_ingestion_component.di_files_metadata(azure_di_metadata)
    # file_metadata = read_json_file(data_ingestion_artifact.metadata_file_path)
    # print(file_metadata['filenames'])
    logger.info("******************* DATA_INGESTION COMPONENT COMPLETED *******************")
    
            

    
    
    
    