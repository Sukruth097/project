import os
import asyncio
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Table, Image, NarrativeText
from langchain_core.prompts import ChatPromptTemplate
from src.config.constants import *
import sys
import base64
from src.exception import PocException
from src.utils import log_execution_time
from src.logger import logger
from tqdm.asyncio import tqdm_asyncio
from src.utils.llmhelper import LLMHelper
from src.utils.prompt_template import tables_summarizer_prompt, images_summarizer_prompt
from openai import AzureOpenAI


os.makedirs(os.path.join(os.getcwd(), "images"), exist_ok=True)

class PDFFileHandler:

    def __init__(self, output_dir):
        self.data_folder = output_dir
        self.files = [file for file in os.listdir(self.data_folder) if file.endswith(".pdf")]
        logger.info(f"Initialized PDFFileHandler with {len(self.files)} PDF files: {self.files}")
        self.llm_model = LLMHelper()
    
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
            raise PocException(e, sys.exc_info())

    @log_execution_time
    async def extract_text_elements(self, raw_pdf_elements, file_name):
        logger.info(f"Extracting text elements from file: {file_name}")
        try:
            text_data = []
            for element in raw_pdf_elements:
                if isinstance(element, NarrativeText):
                    page_number = element.metadata.page_number if hasattr(element.metadata, 'page_number') else None
                    text_content = element.text
                    text_data.append({
                        "source_pdf": file_name,
                        "page_number": page_number,
                        "text": text_content,
                    })
            logger.info(f"Extracted {len(text_data)} text elements from file: {file_name}")
            return text_data
        except Exception as e:
            logger.error(f"Error extracting text elements from file: {file_name}, Error: {e}")
            raise PocException(e, sys.exc_info())

    @log_execution_time
    async def extract_images(self, raw_pdf_elements, file_name):
        logger.info(f"Extracting images from file: {file_name}")
        try:
            images_elements = []
            for element in raw_pdf_elements:
                if "Image" in str(type(element)):
                    page_number = element.metadata.page_number if hasattr(element.metadata, 'page_number') else None
                    image_path = element.metadata.image_path if hasattr(element.metadata, 'image_path') else None

                    if image_path and os.path.exists(image_path):
                        encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('ascii')

                        messages = [
                            {
                                "role": "system",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "You are an AI assistant that helps people find information."
                                    }
                                ]
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "\n"
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpg;base64,{encoded_image}"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": images_summarizer_prompt
                                    }
                                ]
                            }
                        ]
                        client = AzureOpenAI(
                            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
                            api_key=os.getenv("AZURE_OPENAI_API_KEY")
                        )
                        completion = client.chat.completions.create(
                            model="llm-gpt-4o",
                            messages=messages,
                            temperature=0,
                        )
                        description = completion.choices[0].message.content

                        with open(image_path, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

                        images_elements.append({
                            "source_document": "./Share MTS_07_m.pdf",
                            "page_number": page_number,
                            "image_path": image_path,
                            "description": description,
                            "base64_encoding": encoded_string
                        })
            return images_elements
        except Exception as e:
            logger.error(f"Error extracting images from file: {file_name}, Error: {e}")
            raise PocException(e, sys.exc_info())
    
    @log_execution_time
    async def extract_table_elements(self, raw_pdf_elements, file_name):
        logger.info(f"Extracting table elements from file: {file_name}")
        try:
            table_element = []
            table_prompt = ChatPromptTemplate.from_template(tables_summarizer_prompt)

            for element in raw_pdf_elements:
                if isinstance(element, Table):
                    table_page_number = element.metadata.page_number if hasattr(element.metadata, 'page_number') else None
                    table_content = str(element)
                    message = table_prompt.format(table_content=table_content)
                    messages = [{"role": "user", "content": message}]
                    table_description = self.llm_model.get_openai_llm(messages=messages)

                    table_element.append({
                        "page_number": table_page_number,
                        "table_content": table_content,
                        "source_pdf": file_name,
                        "description": table_description
                    })
            logger.info(f"Extracted {len(table_element)} table elements from file: {file_name}")
            return table_element
        except Exception as e:
            logger.error(f"Error extracting table elements from file: {file_name}, Error: {e}")
            raise PocException(e, sys.exc_info())
    
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
            results = await tqdm_asyncio.gather(*tasks, desc="Processing PDFs")
            for text_elements, image_elements, table_elements in results:
                all_text.extend(text_elements)
                all_images.extend(image_elements)
                all_tables.extend(table_elements)
            logger.info(f"Completed extraction of all text and images. Total text elements: {len(all_text)}, Total images: {len(all_images)}, Total tables: {len(all_tables)}")
            return all_text, all_images, all_tables
        except Exception as e:
            logger.error(f"Error extracting all text and images, Error: {e}")
            raise PocException(e, sys.exc_info())

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
            raise PocException(e, sys.exc_info())


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "./data")
    print(os.listdir(path))

    pdf_file_handler = PDFFileHandler(output_dir=path)
    all_text, all_images, all_table = asyncio.run(pdf_file_handler.run_pdf_processing())
    print(all_text[0])
    print(all_images[0]['description'])
    print(all_table[0])
