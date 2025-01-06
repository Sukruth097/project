import weaviate
from src.exception import PocException
import sys
from src.config.constants import *
from dotenv import load_dotenv
import os
import weaviate.classes.config as wc
from weaviate.util import generate_uuid5
from tqdm import tqdm

load_dotenv()

class VectorDatabaseHelper:
    def __init__(self):

        self.weaviate_client = weaviate.connect_to_wcs(
                                cluster_url=os.getenv("WEAVIATE_CLUSTER_URL"),
                                auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
                                headers = {
                                    "X-Azure-Api-Key": os.getenv("AZURE_OPENAI_API_KEY")
                                }
                            )
        
    def define_propeties(self):
        try:
           properties = [
                wc.Property(name="source_document", data_type=wc.DataType.TEXT, skip_vectorization=True),
                wc.Property(name="page_number", data_type=wc.DataType.INT, skip_vectorization=True),
                wc.Property(name="text", data_type=wc.DataType.TEXT),
                wc.Property(name="image_path", data_type=wc.DataType.TEXT, skip_vectorization=True),
                wc.Property(name="description", data_type=wc.DataType.TEXT),
                wc.Property(name="base64_encoding", data_type=wc.DataType.BLOB, skip_vectorization=True),
                wc.Property(name="table_content", data_type=wc.DataType.TEXT),
                # wc.Property(name="url", data_type=wc.DataType.TEXT, skip_vectorization=True),
                # wc.Property(name="audio_path", data_type=wc.DataType.TEXT, skip_vectorization=True),
                # wc.Property(name="transcription", data_type=wc.DataType.TEXT),
                wc.Property(name="content_type", data_type=wc.DataType.TEXT, skip_vectorization=True),
            ]
           return properties
        except Exception as e:
            print(f"Error while defining properties: {str(e)}")
            raise PocException(f"Error while getting vector from Weaviate: {str(e)}")
        
    def w_create_collection(self,collection_name:str=WEAVIATE_COLLECTION_NAME):
        try:
            if collection_name not in self.weaviate_client.collections.list_all():
                self.weaviate_client.collections.create(
                    name=collection_name,
                    properties=self.define_propeties(),
                    vectorizer_config=None
                )
                print(f"Collection '{collection_name}' created successfully.")
            else:
                print(f"Collection '{collection_name}' already exists in Weaviate client.")
        except Exception as e:
            print(f"Error while creating collection: {str(e)}")
            raise PocException(f"Error while creating collection: {str(e)}")
        
    