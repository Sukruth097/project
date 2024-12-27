import os
import uuid
import base64
# from IPython import display
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Table, Image, NarrativeText
from src.config.constants import *
from src.logger import logger
import sys
from src.exception import PocException
from src.utils import log_execution_time
os.makedirs(os.path.join(os.getcwd(), "images"), exist_ok=True)

class PDFFileHanlder:

    def __init__(self, output_dir):
        self.data_folder = output_dir
        self.files = [file for file in os.listdir(self.data_folder) if file.lower().endswith('.pdf')]
        print(f"-------->{self.files}")
    
    @log_execution_time
    def pdf_loader(self, file_name: str):
        try:
            raw_pdf_elements = partition_pdf(
                filename=file_name,
                extract_images_in_pdf=True,
                infer_table_structure=True,
                strategy="hi_res",
                max_characters=4000,
                new_after_n_chars=3800,
                combine_text_under_n_chars=2000,
                extract_image_block_to_payload=False,
                extract_image_block_output_dir="./images",
            )
            return raw_pdf_elements
        except Exception as e:
            print(e)
            raise PocException(e, sys)

    def extract_text_elements(self, raw_pdf_elements):
        try:
            text_data = []
            for element in raw_pdf_elements:
                if isinstance(element, NarrativeText):
                    page_number = element.metadata.page_number
                    text_content = element.text
                    text_data.append({
                        "page_number": page_number,
                        "text": text_content
                    })
            return text_data
        except Exception as e:
            print(e)
            raise PocException(e, sys)

    def extract_images(self, raw_pdf_elements):
        try:
            images_elements = []
            image_page_number = None
            image_path = None
            for element in raw_pdf_elements:
                if isinstance(element, Image):
                    image_page_number = element.metadata.page_number
                    image_path = element.metadata.image_path if hasattr(element.metadata, 'image_path') else None

                images_elements.append({
                    "page_number": image_page_number,
                    "image_path": image_path
                })
            return images_elements
        except Exception as e:
            print(e)
            raise PocException(e, sys)
    
    def extra_table_elements(self, raw_pdf_elements):
        try:
            table_element = []
            for element in raw_pdf_elements:
                if isinstance(element, Table):
                    table_page_number = element.metadata.page_number
                    table_content = str(element)

                    table_element.append({
                        "page_number": table_page_number,
                        "table_content": table_content
                    })
            return table_element
        except Exception as e:
            print(e)
            raise PocException(e)
    
    @log_execution_time
    def extract_all_text_and_images(self):
        try:
            all_text = []
            all_images = []
            all_tables = []
            for file in self.files:
                raw_pdf_elements = self.pdf_loader(os.path.join(self.data_folder, file))
                text_elements = self.extract_text_elements(raw_pdf_elements)
                for text_element in text_elements:
                    all_text.append({
                        "source_document": file,
                        "page_number": text_element["page_number"],
                        "text": text_element["text"]
                    })
                image_elements = self.extract_images(raw_pdf_elements)
                for image_element in image_elements:
                    all_images.append({
                        "source_document": file,
                        "page_number": image_element["page_number"],
                        "image_path": image_element["image_path"]
                    })
                table_elements = self.extra_table_elements(raw_pdf_elements)
                for table_element in table_elements:
                    all_tables.append({
                        "source_document": file,
                        "page_number": table_element["page_number"],
                        "table_content": table_element["table_content"]
                    })
                
            return all_text, all_images, all_tables
        except Exception as e:
            print(e)
            raise PocException(e, sys)

    @log_execution_time
    def run_pdf_processing(self):
        try:
            all_text, all_images, all_tables = self.extract_all_text_and_images()
            return all_text, all_images,all_tables
        except Exception as e:
            print(e)
            raise PocException(e, sys)

if __name__ == "__main__":
    # print(f"-------->{os.getcwd()}")
    path = os.path.join(os.getcwd(), "artifacts/12_25_2024_17_00_49/DataIngestion/rawdata/cracked-output")

    pdf_file_handler = PDFFileHanlder(output_dir=path)
    all_text, all_images,all_table = pdf_file_handler.run_pdf_processing()
    # print(all_text)
    # print(all_images)
    # print(all_table)
    # print(f"-------->{os.getcwd()}")
