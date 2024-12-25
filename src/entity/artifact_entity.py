from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    azure_raw_data :str
    metadata_file_path :str