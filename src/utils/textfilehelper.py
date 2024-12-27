import os
import asyncio
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Table, Image, NarrativeText
from src.config.constants import *
import sys
from src.exception import PocException
from src.utils import log_execution_time
from src.logger import logger
import aiofiles

os.makedirs(os.path.join(os.getcwd(), "images"), exist_ok=True)

class TextFileHandler:

    def __init__(self, output_dir):
        self.data_folder = output_dir
        self.files = [file for file in os.listdir(self.data_folder) if file.lower().endswith('.txt')]
        logger.info(f"Initialized TextFileHandler with {len(self.files)} text files: {self.files}")

    @log_execution_time
    async def text_loader(self, file_name: str):
        logger.info(f"Loading text file: {file_name}")
        try:
            async with aiofiles.open(file_name, 'r') as file:
                content = await file.read()
            logger.info(f"Loaded text file: {file_name}")
            return content
        except Exception as e:
            logger.error(f"Error loading text file: {file_name}, Error: {e}")
            raise PocException(e, sys)

    @log_execution_time
    async def run_text_processing(self):
        logger.info("Starting text processing")
        try:
            all_text = []
            tasks = []
            semaphore = asyncio.Semaphore(5)  # Limit the number of concurrent tasks

            async def process_with_semaphore(file):
                async with semaphore:
                    return await self.text_loader(os.path.join(self.data_folder, file))

            for file in self.files:
                tasks.append(process_with_semaphore(file))
            results = await asyncio.gather(*tasks)
            all_text.extend(results)
            logger.info(f"Completed text processing. Total text files processed: {len(all_text)}")
            return all_text
        except Exception as e:
            logger.error(f"Error in text processing, Error: {e}")
            raise PocException(e, sys)

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "artifacts/12_25_2024_17_00_49/DataIngestion/rawdata/cracked-output")

    text_file_handler = TextFileHandler(output_dir=path)
    all_text_files = asyncio.run(text_file_handler.run_text_processing())
    print(all_text_files)