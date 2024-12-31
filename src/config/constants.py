import time
from datetime import datetime
import os
import socket
# TIMESTAMP = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
TIMESTAMP:str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
ARTIFACT_DIR = os.path.join("artifacts",TIMESTAMP)
USERNAME = socket.gethostname()
DATABASE_NAME="POC"
LOGS_COLLECTION_NAME="logging"
ERROR_COLLECTION_NAME="poc_error_logs"
CONTAINER_NAME="testindex-chunks"
BLOB_NAME="cracked-output"

### Data Ingestion Constants
DATA_INGESTION_ARTIFACT_DIR = 'DataIngestion'
DATA_INGESTION_RAW_DATA_DIR ="rawdata"
DATA_INGESTION_PROCESSED_DATA_DIR ="processed_data"
DATA_INGESTION_PROCESSED_DATA_FILENAME ="processed_data.pdf"
DATA_INGESTION_METADATA_DIR="metadata"
DATA_INGESTION_METADATA_FILENAME="di_metadata.json"

### Data Transformation Constants
DATA_TRANSFORMATION_ARTIFACT_DIR = 'DataTransformation'
DATA_TRANSFORMATION_DATA_DIR = 'data'
for file_type in ['pdf', 'csv', 'pptx', 'docx', 'text']:
    # globals()[f'DATA_TRANSFORMATION_{file_type.upper()}_DIR'] = file_type
    globals()[f'DATA_TRANSFORMATION_{file_type.upper()}_TEXT_FILENAME'] = f'{file_type}_text.json'
    globals()[f'DATA_TRANSFORMATION_{file_type.upper()}_IMAGE_FILENAME'] = f'{file_type}_image.json'
    globals()[f'DATA_TRANSFORMATION_{file_type.upper()}_TABLE_FILENAME'] = f'{file_type}_table.json'
DATA_TRANSFORMATION_METADATA_DIR="metadata"
DATA_TRANSFORMATION_METADATA_FILENAME="dt_metadata.json"
DATA_TRANSFORMATION_TEXT_FILE ="pdf_text"
DATA_TRANSFORMATION_IMAGE_FILE ="image_text"
DATA_TRANSFORMATION_TABLE_FILE ="table_text"





