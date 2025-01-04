import weaviate
from src.exception import PocException
import sys

class VectorDatabase:
    def __init__(self, client):
        self.client = client

    def get_vector(self, id):
        try:
            response = self.client.query.get(id)
            return response['data']['Get']['vector']
        except Exception as e:
            print(f"Error during getting vector: {e}")
            raise PocException(e, sys)

    # def get_vector_by_class(self, class