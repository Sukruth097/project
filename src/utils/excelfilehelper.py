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

class ExcelFileHandler:
        
        def __init__(self, output_dir):
            self.data_folder = output_dir
            self.files = [file for file in os.listdir(self.data_folder) if file.lower().endswith('.xlsx')]
            logger.info(f"Initialized ExcelFileHandler with {len(self.files)} xlsx files: {self.files}")

        @log_execution_time
        async def xlsx_loader(self, file_name: str):
            logger.info(f"Loading xlsx file: {file_name}")
            try:
                content = await asyncio.to_thread(UnstructuredExcelLoader, file_name)
                logger.info(f"Loaded xlsx file: {file_name}")
                return content
            except Exception as e:
                logger.error(f"Error loading xlsx file: {file_name}, Error: {e}")
                raise PocException(e, sys)

        @log_execution_time
        async def run_xlsx_processing(self):
            logger.info("Starting xlsx processing")
            try:
                all_text = []
                tasks = []
                semaphore = asyncio.Semaphore(5)  # Limit the number of concurrent tasks

                async def process_with_semaphore(file):
                    async with semaphore:
                        return await self.xlsx_loader(os.path.join(self.data_folder, file))

                for file in self.files:
                    tasks.append(process_with_semaphore(file))
                results = await asyncio.gather(*tasks)
                all_text.extend(results)
                logger.info(f"Completed xlsx processing. Total xlsx files processed: {len(all_text)}")
                return all_text
            except Exception as e:
                logger.error(f"Error in xlsx processing, Error: {e}")
                raise PocException(e, sys)

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "artifacts/12_25_2024_17_00_49/DataIngestion/rawdata/cracked-output")
    xlsx_file_handler = ExcelFileHandler(output_dir=path)
    all_xlsx_files = asyncio.run(xlsx_file_handler.run_xlsx_processing())
    print(all_xlsx_files)
    