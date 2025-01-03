from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    azure_raw_data :str
    metadata_file_path :str

@dataclass
class DataTransformationArtifact:
    pdf_data :str
    image_data :str
    table_data :str
