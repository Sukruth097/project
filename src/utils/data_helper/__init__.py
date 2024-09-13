from langchain_community.llms import Ollama
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
from langchain_experimental.text_splitter import SemanticChunker
from src.logger import logger
from src.exception import PocException
from src.utils import log_execution_time

FILE_LOADERS = {
    "csv": CSVLoader,
    "docx": Docx2txtLoader,
    "pdf": PyMuPDFLoader,
    "pptx": UnstructuredPowerPointLoader,
    "txt": TextLoader,
    "xlsx": UnstructuredExcelLoader,
}

ACCEPTED_FILE_TYPES = list(FILE_LOADERS)
