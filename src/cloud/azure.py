from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from datetime import datetime
import time

class AzureBlobManager:
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def download_file(self, container_name, blob_name, download_path):
        start_time = time.time()
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        end_time = time.time()
        print(f"Downloaded {blob_name} to {download_path}")
        metadata = self.get_metadata(container_name, blob_name)
        metadata["time_taken"] = end_time - start_time
        print(f"Metadata: {metadata}")

    def download_multiple_files(self, container_name, blob_names, download_dir):
        for blob_name in blob_names:
            download_path = os.path.join(download_dir, os.path.basename(blob_name))
            self.download_file(container_name, blob_name, download_path)

    def upload_files(self, container_name, file_paths, blob_names):
        container_client = self.blob_service_client.get_container_client(container_name)
        for file_path, blob_name in zip(file_paths, blob_names):
            start_time = time.time()
            blob_client = container_client.get_blob_client(blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            end_time = time.time()
            print(f"Uploaded {file_path} to {blob_name}")
            metadata = self.get_metadata(container_name, blob_name)
            metadata["time_taken"] = end_time - start_time
            print(f"Metadata: {metadata}")

    def get_metadata(self, container_name, blob_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        properties = blob_client.get_blob_properties()
        metadata = {
            "container": container_name,  # Added container name to metadata
            "name": blob_name,
            "size": properties.size,
            "last_modified": properties.last_modified,
            "content_type": properties.content_settings.content_type
        }
        return metadata

# Example usage:
# azure_blob_manager = AzureBlobManager("your_connection_string")
# azure_blob_manager.download_file("your_container_name", "example_blob.txt", "local_path.txt")
# azure_blob_manager.download_files("your_container_name", ["blob1.txt", "blob2.txt"], "local_directory")
# azure_blob_manager.upload_files("your_container_name", ["local_file1.txt", "local_file2.txt"], ["uploaded_blob1.txt", "uploaded_blob2.txt"])
# metadata = azure_blob_manager.get_metadata("your_container_name", "example_blob.txt")
# print(metadata)
