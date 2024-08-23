from openai import AzureOpenAI

client = AzureOpenAI(
        api_key="b614b5b86d9e4baba98dbc28b802ed26",
        api_version="2024-02-01",
        azure_endpoint="https://petofy-openai.openai.azure.com/",
    )

vectors = []


def generate_embeddings(chunk):
    vector_data = client.embeddings.create(input=chunk, model="text-embedding")
    return vector_data.data[0].embedding
