import weaviate
from src.exception import PocException
from src.config.constants import *
from src.logger import logger
from dotenv import load_dotenv
import os
import weaviate.classes.config as wc
from weaviate.util import generate_uuid5
from tqdm import tqdm
from .llmhelper import LLMHelper

load_dotenv()

class VectorDatabaseHelper:
    def __init__(self):
        logger.info("Initializing VectorDatabaseHelper")
        self.weaviate_client = weaviate.connect_to_wcs(
            cluster_url=os.getenv("WEAVIATE_CLUSTER_URL"),
            auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
            headers={"X-Azure-Api-Key": os.getenv("AZURE_OPENAI_API_KEY")}
        )
        logger.info("Weaviate client initialized")
        self.llm_helper = LLMHelper()
        self.embedding_model = self.llm_helper.generate_openai_embeddings()
        logger.info("LLMHelper and embedding model initialized")

    def define_properties(self):
        logger.info("Defining properties")
        try:
            properties = [
                wc.Property(name="source_document", data_type=wc.DataType.TEXT, skip_vectorization=True),
                wc.Property(name="page_number", data_type=wc.DataType.INT, skip_vectorization=True),
                wc.Property(name="text", data_type=wc.DataType.TEXT),
                wc.Property(name="image_path", data_type=wc.DataType.TEXT, skip_vectorization=True),
                wc.Property(name="description", data_type=wc.DataType.TEXT),
                wc.Property(name="base64_encoding", data_type=wc.DataType.BLOB, skip_vectorization=True),
                wc.Property(name="table_content", data_type=wc.DataType.TEXT),
                wc.Property(name="content_type", data_type=wc.DataType.TEXT, skip_vectorization=True),
            ]
            logger.info(f"Properties defined: {properties}")
            return properties
        except Exception as e:
            logger.error(f"Error while defining properties: {str(e)}")
            raise PocException(f"Error while defining properties: {str(e)}")

    def w_create_collection(self, collection_name: str = WEAVIATE_COLLECTION_NAME):
        logger.info(f"Creating collection: {collection_name}")
        try:
            if collection_name not in self.weaviate_client.collections.list_all():
                logger.info(f"Collection '{collection_name}' does not exist. Creating new collection.")
                self.weaviate_client.collections.create(
                    name=collection_name,
                    properties=self.define_properties(),
                    vectorizer_config=None
                )
                logger.info(f"Collection '{collection_name}' created successfully.")
            else:
                logger.info(f"Collection '{collection_name}' already exists in Weaviate client.")
            collection = self.weaviate_client.collections.get(collection_name)
            logger.info(f"Collection retrieved: {collection}")
            return collection
        except Exception as e:
            logger.error(f"Error while creating collection: {str(e)}")
            raise PocException(f"Error while creating collection: {str(e)}")

    def ingest_text_data(self, collection, text_data):
        logger.info("Ingesting text data")
        try:
            with collection.batch.dynamic() as batch:
                for text in tqdm(text_data, desc="Ingesting text data"):
                    logger.info(f"Ingesting text: {text}")
                    vector = self.embedding_model(text['text'])
                    logger.info(f"Generated vector: {vector}")
                    text_obj = {
                        "source_document": text['source_document'],
                        "page_number": text['page_number'],
                        "text": text['text'],
                        "content_type": "text"
                    }
                    logger.info(f"Text object: {text_obj}")
                    batch.add_object(
                        properties=text_obj,
                        uuid=generate_uuid5(f"{text['source_document']}_{text['page_number']}_{text['paragraph_number']}"),
                        vector=vector
                    )
                    logger.info("Text object added to batch")
        except Exception as e:
            logger.error(f"Error while ingesting text data: {str(e)}")
            raise PocException(f"Error while ingesting text data: {str(e)}")

    def ingest_image_data(self, collection, image_data):
        logger.info("Ingesting image data")
        try:
            with collection.batch.dynamic() as batch:
                for image in tqdm(image_data, desc="Ingesting image data"):
                    logger.info(f"Ingesting image: {image}")
                    vector = self.embedding_model(image['description'])
                    logger.info(f"Generated vector: {vector}")
                    image_obj = {
                        "source_document": image['source_document'],
                        "page_number": image['page_number'],
                        "image_path": image['image_path'],
                        "description": image['description'],
                        "base64_encoding": image['base64_encoding'],
                        "content_type": "image"
                    }
                    logger.info(f"Image object: {image_obj}")
                    batch.add_object(
                        properties=image_obj,
                        uuid=generate_uuid5(f"{image['source_document']}_{image['page_number']}_{image['image_path']}"),
                        vector=vector
                    )
                    logger.info("Image object added to batch")
        except Exception as e:
            logger.error(f"Error while ingesting image data: {str(e)}")
            raise PocException(f"Error while ingesting image data: {str(e)}")

    def ingest_table_data(self, collection, table_data):
        logger.info("Ingesting table data")
        try:
            with collection.batch.dynamic() as batch:
                for table in tqdm(table_data, desc="Ingesting table data"):
                    logger.info(f"Ingesting table: {table}")
                    vector = self.embedding_model(table['description'])
                    logger.info(f"Generated vector: {vector}")
                    table_obj = {
                        "source_document": table['source_document'],
                        "page_number": table['page_number'],
                        "table_content": table['table_content'],
                        "description": table['description'],
                        "content_type": "table"
                    }
                    logger.info(f"Table object: {table_obj}")
                    batch.add_object(
                        properties=table_obj,
                        uuid=generate_uuid5(f"{table['source_document']}_{table['page_number']}"),
                        vector=vector
                    )
                    logger.info("Table object added to batch")
        except Exception as e:
            logger.error(f"Error while ingesting table data: {str(e)}")
            raise PocException(f"Error while ingesting table data: {str(e)}")

    def ingest_all_data(self, collection_name, text_data, image_data, table_data):
        logger.info(f"Ingesting all data into collection: {collection_name}")
        try:
            collection = self.w_create_collection(collection_name)
            logger.info("Ingesting text data")
            self.ingest_text_data(collection, text_data)
            logger.info("Ingestion of text data is completed")
            logger.info("Ingesting image data")
            self.ingest_image_data(collection, image_data)
            logger.info("Ingestion of image data is completed")
            logger.info("Ingesting table data")
            self.ingest_table_data(collection, table_data)
            logger.info("Ingestion of table data is completed")
            print("Succesfully ingested all the data")

            if len(collection.batch.failed_objects) > 0:
                logger.error(f"Failed to import {len(collection.batch.failed_objects)} objects")
            else:
                logger.info("All objects imported successfully")
        except Exception as e:
            logger.error(f"Error while ingesting all data: {str(e)}")
            raise PocException(f"Error while ingesting all data: {str(e)}")
