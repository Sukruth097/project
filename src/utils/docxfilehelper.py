import os
import asyncio
from src.config.constants import *
import sys
from src.exception import PocException
from src.utils import log_execution_time
from src.logger import logger
from langchain_community.document_loaders import Docx2txtLoader

os.makedirs(os.path.join(os.getcwd(), "images"), exist_ok=True)

class DocxFileHandler:

    def __init__(self, output_dir):
        self.data_folder = output_dir
        self.files = [file for file in os.listdir(self.data_folder) if file.lower().endswith('.docx')]
        logger.info(f"Initialized DocxFileHandler with {len(self.files)} docx files: {self.files}")

    @log_execution_time
    async def docx_loader(self, file_name: str):
        logger.info(f"Loading docx file: {file_name}")
        try:
            content = await load_with_docx2txt_loader(file_name)
            logger.info(f"Loaded docx file: {file_name}")
            return content
        except Exception as e:
            logger.error(f"Error loading docx file: {file_name}, Error: {e}")
            raise PocException(e, sys)

    @log_execution_time
    async def run_docx_processing(self):
        logger.info("Starting docx processing")
        try:
            all_text = []
            tasks = []
            semaphore = asyncio.Semaphore(5)  # Limit the number of concurrent tasks

            async def process_with_semaphore(file):
                async with semaphore:
                    return await self.docx_loader(os.path.join(self.data_folder, file))

            for file in self.files:
                tasks.append(process_with_semaphore(file))
            results = await asyncio.gather(*tasks)
            all_text.extend(results)
            logger.info(f"Completed docx processing. Total docx files processed: {len(all_text)}")
            return all_text
        except Exception as e:
            logger.error(f"Error in docx processing, Error: {e}")
            raise PocException(e, sys)

async def load_with_docx2txt_loader(file_path):
    loader = Docx2txtLoader(file_path)
    return await asyncio.to_thread(loader.load)

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "artifacts/12_25_2024_17_00_49/DataIngestion/rawdata/cracked-output")
    docx_file_handler = DocxFileHandler(output_dir=path)
    all_docx_files = asyncio.run(docx_file_handler.run_docx_processing())
    print(all_docx_files)
