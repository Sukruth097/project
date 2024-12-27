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

class PowerPointFileHandler:

        def __init__(self, output_dir):
            self.data_folder = output_dir
            self.files = [file for file in os.listdir(self.data_folder) if file.lower().endswith('.pptx')]
            logger.info(f"Initialized PowerPointFileHandler with {len(self.files)} pptx files: {self.files}")

        @log_execution_time
        async def pptx_loader(self, file_name: str):
            logger.info(f"Loading pptx file: {file_name}")
            try:
                content = await asyncio.to_thread(UnstructuredPowerPointLoader, file_name)
                logger.info(f"Loaded pptx file: {file_name}")
                return content
            except Exception as e:
                logger.error(f"Error loading pptx file: {file_name}, Error: {e}")
                raise PocException(e, sys)

        @log_execution_time
        async def run_pptx_processing(self):
            logger.info("Starting pptx processing")
            try:
                all_text = []
                tasks = []
                semaphore = asyncio.Semaphore(5)  # Limit the number of concurrent tasks

                async def process_with_semaphore(file):
                    async with semaphore:
                        return await self.pptx_loader(os.path.join(self.data_folder, file))

                for file in self.files:
                    tasks.append(process_with_semaphore(file))
                results = await asyncio.gather(*tasks)
                all_text.extend(results)
                logger.info(f"Completed pptx processing. Total pptx files processed: {len(all_text)}")
                return all_text
            except Exception as e:
                logger.error(f"Error in pptx processing, Error: {e}")
                raise PocException(e, sys)

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "artifacts/12_25_2024_17_00_49/DataIngestion/rawdata/cracked-output")
    pptx_file_handler = PowerPointFileHandler(output_dir=path)
    all_pptx_files = asyncio.run(pptx_file_handler.run_pptx_processing())
    print(all_pptx_files)