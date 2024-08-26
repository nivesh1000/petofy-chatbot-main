from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

vectors = []


def generate_embeddings(chunk):
    vector_data = client.embeddings.create(input=chunk, model="text-embedding")
    return vector_data.data[0].embedding
