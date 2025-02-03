import os
from dotenv import load_dotenv
from src.utils.llmhelper import LLMHelper
from src.utils.vectordbhelper import VectorDatabaseHelper
from src.exception import PocException


class Rag:
    def __init__(self):
        self.llm_helper = LLMHelper()
        self.vector_db_helper = VectorDatabaseHelper()
        self.embedding_model = self.llm_helper.generate_openai_embeddings()

    def retrive_data(self,query):
        try:
            query_embedding = self.llm_helper.generate_openai_embeddings(query)
            
            
        except Exception as e:
            raise PocException(e)
            print(e)
        