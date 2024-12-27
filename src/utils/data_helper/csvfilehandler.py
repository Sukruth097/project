import os
import asyncio
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Table, Image, NarrativeText
from src.config.constants import *
import sys
from src.exception import PocException
from src.utils import log_execution_time
from src.logger import logger
import pandas as pd

os.makedirs(os.path.join(os.getcwd(), "images"), exist_ok=True)

class CSVFileHandler:

            def __init__(self, output_dir):
                self.data_folder = output_dir
                self.files = [file for file in os.listdir(self.data_folder) if file.lower().endswith('.csv')]
                logger.info(f"Initialized CSVFileHandler with {len(self.files)} csv files: {self.files}")

            @log_execution_time
            async def csv_loader(self, file_name: str):
                logger.info(f"Loading csv file: {file_name}")
                try:
                    content = await asyncio.to_thread(pd.read_csv, file_name)
                    logger.info(f"Loaded csv file: {file_name}")
                    return content
                except Exception as e:
                    logger.error(f"Error loading csv file: {file_name}, Error: {e}")
                    raise PocException(e, sys)

            @log_execution_time
            async def run_csv_processing(self):
                logger.info("Starting csv processing")
                try:
                    all_data = []
                    tasks = []
                    semaphore = asyncio.Semaphore(5)  # Limit the number of concurrent tasks

                    async def process_with_semaphore(file):
                        async with semaphore:
                            return await self.csv_loader(os.path.join(self.data_folder, file))

                    for file in self.files:
                        tasks.append(process_with_semaphore(file))
                    results = await asyncio.gather(*tasks)
                    all_data.extend(results)
                    logger.info(f"Completed csv processing. Total csv files processed: {len(all_data)}")
                    return all_data
                except Exception as e:
                    logger.error(f"Error in csv processing, Error: {e}")
                    raise PocException(e, sys)
                
if __name__ == "__main__":
            
            path = os.path.join(os.getcwd(), "artifacts/12_25_2024_17_00_49/DataIngestion/rawdata/cracked-output")
            csv_file_handler = CSVFileHandler(output_dir=path)
            all_csv_files = asyncio.run(csv_file_handler.run_csv_processing())
            print(all_csv_files)