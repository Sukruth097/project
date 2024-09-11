from src.logger import logger
from src.exception import PocException
import os
import sys
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.utils import log_execution_time
from src.config.azure_config import AzureBlobManager
from src.config.constants import *


class DataIngestion:
    
    @log_execution_time
    def __init__(self, data_ingestion_config:DataIngestionConfig,azure_blob_config):
        logger.info("******************* DATA_INGESTION COMPONENT STARTED *******************")
        self.data_ingestion_config=data_ingestion_config
        self.azure_blob_config = azure_blob_config
        
    @log_execution_time    
    def download_azure_data(self):
        try:
            download_dir = self.data_ingestion_config.raw_data_dir
            # logger.info(f"Creating the directory:{download_dir} to store the data")
            # os.makedirs(download_dir,exist_ok=True)
            # logger.info(f"Successfully created the directory:{download_dir} to store the data")
            azure_container_name = self.data_ingestion_config.azure_container_name
            azure_blob_name = self.data_ingestion_config.azure_blob_name
            logger.info(f"Starting downloading the files from azure conatiner:{azure_container_name} and azure blob:{azure_blob_name}")
            raw_data_path = self.azure_blob_config.download_allfiles_in_blob(azure_container_name,download_dir,azure_blob_name)
            logger.info(f" Succesfully downloaded all the files and stored in {raw_data_path}")
            return raw_data_path
        except Exception as e:
            logger.error(e)
            PocException(e,sys)
    
    @log_execution_time
    def preprocessed_data(self):
        try:
            pass
        except Exception as e:
            PocException(e,sys)
            
    @log_execution_time
    def capture_di_metadata(self):
        try:
            pass
        except Exception as e:
            PocException(e,sys)
    
    @log_execution_time
    def trigger_data_ingestion(self):
        try:
            azure_raw_data = self.download_azure_data()
        except Exception as e:
            PocException(e,sys)
            
            
if __name__ == "__main__":
    data_ingestion_config= DataIngestionConfig()
    azure_blob_config = AzureBlobManager()
    data_ingestion_component = DataIngestion(data_ingestion_config,azure_blob_config)
    data_ingestion_component.download_azure_data()
    logger.info("******************* DATA_INGESTION COMPONENT COMPLETED *******************")
    
            

    
    
    
    