from openai import AzureOpenAI
import google.generativeai as genai
import os
from groq import Groq


class LLMs:

    def __init__(self, azure_openai_key, gemini_pro_key, grog_llama_key):
        self.azure_openai_key = azure_openai_key
        self.gemini_pro_key = gemini_pro_key
        self.grog_llama_key = grog_llama_key

    def azure_openai(self):
        
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version="2024-10-21",
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            )
        
        response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "When was Microsoft founded?"}
        ]
        )

        return response.choices[0].message.content

    def gemini_pro(self, search_indexes):
        
        genai.configure(api_key="YOUR_API_KEY")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Explain how AI works")

        return response.text.strip()

    def grog_llama(self, search_indexes):
        # Assuming grog_llama has a similar API to OpenAI
        client = Groq(
                api_key=os.environ.get("GROQ_API_KEY"),
                )
 
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain the importance of fast language models",
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content