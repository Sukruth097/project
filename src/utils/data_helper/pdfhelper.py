import os
import asyncio
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Table, Image, NarrativeText
from src.config.constants import *
import sys
from src.exception import PocException
from src.utils import log_execution_time
from src.logger import logger
os.makedirs(os.path.join(os.getcwd(), "images"), exist_ok=True)

class PDFFileHandler:

    def __init__(self, output_dir):
        self.data_folder = output_dir
        self.files = [file for file in os.listdir(self.data_folder) if file.lower().endswith('.pdf')]
        logger.info(f"Initialized PDFFileHandler with {len(self.files)} PDF files: {self.files}")
    
    @log_execution_time
    async def pdf_loader(self, file_name: str):
        logger.info(f"Loading PDF file: {file_name}")
        try:
            raw_pdf_elements = await asyncio.to_thread(partition_pdf,
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
            logger.info(f"Loaded PDF file: {file_name}")
            return raw_pdf_elements
        except Exception as e:
            logger.error(f"Error loading PDF file: {file_name}, Error: {e}")
            raise PocException(e, sys)

    @log_execution_time
    async def extract_text_elements(self, raw_pdf_elements, file_name):
        logger.info(f"Extracting text elements from file: {file_name}")
        try:
            text_data = []
            for element in raw_pdf_elements:
                if isinstance(element, NarrativeText):
                    page_number = element.metadata.page_number
                    text_content = element.text
                    text_data.append({
                        "page_number": page_number,
                        "text": text_content,
                        "source_pdf": file_name
                    })
            logger.info(f"Extracted {len(text_data)} text elements from file: {file_name}")
            return text_data
        except Exception as e:
            logger.error(f"Error extracting text elements from file: {file_name}, Error: {e}")
            raise PocException(e, sys)

    @log_execution_time
    async def extract_images(self, raw_pdf_elements, file_name):
        logger.info(f"Extracting images from file: {file_name}")
        try:
            images_elements = []
            for element in raw_pdf_elements:
                if isinstance(element, Image):
                    image_page_number = element.metadata.page_number
                    image_path = element.metadata.image_path if hasattr(element.metadata, 'image_path') else None

                    images_elements.append({
                        "page_number": image_page_number,
                        "image_path": image_path,
                        "source_pdf": file_name
                    })
            logger.info(f"Extracted {len(images_elements)} images from file: {file_name}")
            return images_elements
        except Exception as e:
            logger.error(f"Error extracting images from file: {file_name}, Error: {e}")
            raise PocException(e, sys)
    
    @log_execution_time
    async def extract_table_elements(self, raw_pdf_elements, file_name):
        logger.info(f"Extracting table elements from file: {file_name}")
        try:
            table_element = []
            for element in raw_pdf_elements:
                if isinstance(element, Table):
                    table_page_number = element.metadata.page_number
                    table_content = str(element)

                    table_element.append({
                        "page_number": table_page_number,
                        "table_content": table_content,
                        "source_pdf": file_name
                    })
            logger.info(f"Extracted {len(table_element)} table elements from file: {file_name}")
            return table_element
        except Exception as e:
            logger.error(f"Error extracting table elements from file: {file_name}, Error: {e}")
            raise PocException(e)
    
    @log_execution_time
    async def extract_all_text_and_images(self):
        logger.info("Starting extraction of all text and images")
        try:
            all_text = []
            all_images = []
            all_tables = []
            tasks = []
            semaphore = asyncio.Semaphore(5)  # Limit the number of concurrent tasks

            async def process_with_semaphore(file):
                async with semaphore:
                    return await self.process_file(file)

            for file in self.files:
                tasks.append(process_with_semaphore(file))
            results = await asyncio.gather(*tasks)
            for text_elements, image_elements, table_elements in results:
                all_text.extend(text_elements)
                all_images.extend(image_elements)
                all_tables.extend(table_elements)
            logger.info(f"Completed extraction of all text and images. Total text elements: {len(all_text)}, Total images: {len(all_images)}, Total tables: {len(all_tables)}")
            return all_text, all_images, all_tables
        except Exception as e:
            logger.error(f"Error extracting all text and images, Error: {e}")
            raise PocException(e, sys)

    @log_execution_time
    async def process_file(self, file):
        logger.info(f"Processing file: {file}")
        raw_pdf_elements = await self.pdf_loader(os.path.join(self.data_folder, file))
        text_task = self.extract_text_elements(raw_pdf_elements, file)
        image_task = self.extract_images(raw_pdf_elements, file)
        table_task = self.extract_table_elements(raw_pdf_elements, file)
        text_elements, image_elements, table_elements = await asyncio.gather(text_task, image_task, table_task)
        logger.info(f"Completed processing file: {file}. Extracted {len(text_elements)} text elements, {len(image_elements)} images, and {len(table_elements)} tables.")
        return text_elements, image_elements, table_elements

    @log_execution_time
    async def run_pdf_processing(self):
        logger.info("Starting PDF processing")
        try:
            all_text, all_images, all_tables = await self.extract_all_text_and_images()
            logger.info("Completed PDF processing")
            return all_text, all_images, all_tables
        except Exception as e:
            logger.error(f"Error in PDF processing, Error: {e}")
            raise PocException(e, sys)


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "artifacts/12_25_2024_17_00_49/DataIngestion/rawdata/cracked-output")

    pdf_file_handler = PDFFileHandler(output_dir=path)
    all_text, all_images, all_table = asyncio.run(pdf_file_handler.run_pdf_processing())
    print(all_text)
    print(all_images)
    print(all_table)


        

        

       
        

        