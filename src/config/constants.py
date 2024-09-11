import time
from datetime import datetime
import os
# TIMESTAMP = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
TIMESTAMP:str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
ARTIFACT_DIR = os.path.join("artifacts",TIMESTAMP)
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

