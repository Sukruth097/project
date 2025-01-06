from openai import AzureOpenAI
import google.generativeai as genai
import os
from groq import Groq
from src.config.constants import *
from dotenv import load_dotenv

load_dotenv()

class LLMHelper:
    def __init__(self,auth_type_keys):
        self.auth_type_keys = auth_type_keys
        self.token_provider = AZURE_TOKEN_PROVIDER

        if self.auth_type_keys:
            self.openai_client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY")
            )
        else:
            self.openai_client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
                azure_ad_token_provider=self.token_provider,
            )

        # self.genai_client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
        # self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def get_openai_llm(self, messages):
        completion = self.openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=AZURE_OPENAI_TEMPERATURE,
            max_tokens=AZURE_OPENAI_MAXTOKENS,
            messages=messages
        )
        return completion

    def generate_openai_embeddings(self, data):
        embedding = self.openai_client.embeddings.create(
            model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
            input=data
        )
        return embedding.data[0].embedding

    # def get_genai_response(self, prompt):
    #     response = self.genai_client.generate(
    #         model=GENAI_MODEL_NAME,
    #         prompt=prompt,
    #         temperature=GENAI_TEMPERATURE,
    #         max_tokens=GENAI_MAXTOKENS
    #     )
    #     return response

    # def generate_groq_embeddings(self, data):
    #     embedding = self.groq_client.embeddings.create(
    #         model=GROQ_MODEL_NAME,
    #         input=data
    #     )
    #     return embedding.data[0].embedding