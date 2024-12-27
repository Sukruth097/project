from langchain_community.llms import Ollama
import os
from PIL import Image
import io
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    CSVLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredPowerPointLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
)
from unstructured.partition.pdf import partition_pdf
from langchain_experimental.text_splitter import SemanticChunker
from src.logger import logger
from src.exception import PocException
from src.utils import log_execution_time

FILE_LOADERS = {
    "csv": CSVLoader,
    "docx": Docx2txtLoader,
    "pdf": partition_pdf,
    "pptx": UnstructuredPowerPointLoader,
    "txt": TextLoader,
    "xlsx": UnstructuredExcelLoader,
}

def file_type_acceptance_list():
    """
    provide the list of accepted file types
    """
    accepted_file_list = list(FILE_LOADERS)
    return accepted_file_list


class ChatWithFile:
    """
    Main class to handle the interface with the LLM
    """
    def __init__(self, file_path, file_type):
        """
        Perform initial parsing of the uploaded file and initialize the
        chat instance.

        :param file_path: Full path and name of uploaded file
        :param file_type: File extension determined
        """
        self.embedding_model = self.load_embedding_model()
        self.vectordb = None
        loader = FILE_LOADERS[file_type](file_path=file_path)
        pages = loader.load_and_split()
        docs = self.split_into_chunks(pages)
        self.store_in_chroma(docs)

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.llm = ""