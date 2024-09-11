from collections import namedtuple
from datetime import datetime
from src.config.constants import *
import os

DataIngestionArtifact = namedtuple("DataIngestionArtifact",
                                   ["feature_store_file_path", "metadata_file_path", "download_dir"])

class TrainingDataConfig:

    def __init__(self):
        self.client_data_artifact_dir = os.path.join(ARTIFACT_DIR)


class DataIngestionConfig():

    def __init__(self):
        self.data_ingestion_dir = os.path.join(ARTIFACT_DIR,DATA_INGESTION_ARTIFACT_DIR)
        self.raw_data_dir = os.path.join(self.data_ingestion_dir,DATA_INGESTION_RAW_DATA_DIR)
        self.processed_data_dir = os.path.join(self.data_ingestion_dir,DATA_INGESTION_PROCESSED_DATA_DIR)
        self.processed_data_filename = DATA_INGESTION_PROCESSED_DATA_FILENAME
        self.azure_container_name = CONTAINER_NAME
        self.azure_blob_name = BLOB_NAME