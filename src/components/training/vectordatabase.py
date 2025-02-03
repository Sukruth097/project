import weaviate
from src.exception import PocException
import sys
from src.utils.vectordbhelper import VectorDatabaseHelper
from src.entity.artifact_entity import DataTransformationArtifact

class VectorDatabase:
    def __init__(self, vectordatabase_config,data_transformation_artifact:DataTransformationArtifact):
        self.vectordatabase_config = vectordatabase_config,
        self.data_transformation_artifact = data_transformation_artifact
        self.vectordb = VectorDatabaseHelper()

    
    def store_records_to_db(self,collection_name):
        try:
            text = self.data_transformation_artifact.text_data
            image = self.data_transformation_artifact.image_data
            table = self.data_transformation_artifact.table_data
            
            self.vectordb.ingest_all_data(collection_name=collection_name,text_data=text,image_data=image,table_data=table)
        except Exception as e:
            raise PocException(e)
            print(PocException(e))

if __name__ == "__main__":
    dta = DataTransformationArtifact()
    vcc = "vectordatabase_config"
    svb= VectorDatabase(vcc,dta)
    svb.store_records_to_db(collection_name="rag")



    
        

    

