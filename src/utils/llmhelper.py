from openai import AzureOpenAI
import os
from src.config.constants import *
from dotenv import load_dotenv
from src.logger import logger
from src.exception import PocException
import openai
import base64

load_dotenv()

class LLMHelper:
    def __init__(self):
        self.openai_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )

    def get_openai_llm(self, messages):
        try:
            logger.info("Requesting OpenAI LLM with messages: %s", messages)
            completion = self.openai_client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT_NAME,
                temperature=AZURE_OPENAI_TEMPERATURE,
                max_tokens=AZURE_OPENAI_MAXTOKENS,
                messages=messages
            )
            logger.info("Received OpenAI LLM response: %s", completion)
            return completion.choices[0].message
        except openai.APIConnectionError as e:
            logger.error("APIConnectionError in get_openai_llm: %s", str(e))
            raise PocException("Failed to get OpenAI LLM response due to connection error") from e
        except openai.RateLimitError as e:
            logger.error("RateLimitError in get_openai_llm: %s", str(e))
            raise PocException("Failed to get OpenAI LLM response due to rate limit") from e
        except openai.APIStatusError as e:
            logger.error("APIStatusError in get_openai_llm: %s", str(e))
            raise PocException("Failed to get OpenAI LLM response due to API status error") from e
        except Exception as e:
            logger.error("Error in get_openai_llm: %s", str(e))
            raise PocException("Failed to get OpenAI LLM response") from e

    def generate_openai_embeddings(self, data=None):
        try:
            logger.info("Generating OpenAI embeddings for data: %s", data)
            embedding = self.openai_client.embeddings.create(
                model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
                input=data
            )
            logger.info("Received OpenAI embeddings response: %s", embedding)
            return embedding.data[0].embedding
        except openai.APIConnectionError as e:
            logger.error("APIConnectionError in generate_openai_embeddings: %s", str(e))
            raise PocException("Failed to generate OpenAI embeddings due to connection error") from e
        except openai.RateLimitError as e:
            logger.error("RateLimitError in generate_openai_embeddings: %s", str(e))
            raise PocException("Failed to generate OpenAI embeddings due to rate limit") from e
        except openai.APIStatusError as e:
            logger.error("APIStatusError in generate_openai_embeddings: %s", str(e))
            raise PocException("Failed to generate OpenAI embeddings due to API status error") from e
        except Exception as e:
            logger.error("Error in generate_openai_embeddings: %s", str(e))
            raise PocException("Failed to generate OpenAI embeddings") from e

    def azureopenai_with_image(self,encoded_image,images_summarizer_prompt):
        try: 
            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps people find information."
                },
                {
                    "role": "user",
                    "content": f"data:image/jpg;base64,{encoded_image}\n{images_summarizer_prompt}"
                }
            ]
   
            completion = self.openai_client.chat.completions.create(  
                model=AZURE_OPENAI_DEPLOYMENT_NAME,  
                messages=messages,  
                temperature=0
            )
            description = completion.choices[0].message.content
            logger.info("Received OpenAI response for image: %s", description)
            return description
        except openai.APIConnectionError as e:
            logger.error("APIConnectionError in azureopenai_with_image: %s", str(e))
            raise PocException("Failed to get OpenAI response for image due to connection error") from e
        except openai.RateLimitError as e:
            logger.error("RateLimitError in azureopenai_with_image: %s", str(e))
            raise PocException("Failed to get OpenAI response for image due to rate limit") from e
        except openai.APIStatusError as e:
            logger.error("APIStatusError in azureopenai_with_image: %s", str(e))
            raise PocException("Failed to get OpenAI response for image due to API status error") from e
        except Exception as e:
            logger.error("Error in azureopenai_with_image: %s", str(e))
            raise PocException("Failed to get OpenAI response for image") from e
