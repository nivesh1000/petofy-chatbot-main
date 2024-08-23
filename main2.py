from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from vector2 import BeckHealthVectorSearch
load_dotenv()

def completion():
    service_endpoint =os.getenv("SERVICE_ENDPOINT")
    key = os.getenv("RESOURCE_KEY")
    deployment = "gpt-35-turbo"

    client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        ) 

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": "price of mircochip",
            },
        ],
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": service_endpoint,
                        "index_name": "petofy-vector-data",
                        "authentication": {
                            "type": "api_key",
                            "key": key,
                        },
                    },
                }
            ],
        },
    )

    print(completion.choices[0].message.content)

# completion()

def generate_response():
    query="what is microchip?"
    search_engine=BeckHealthVectorSearch()
    search_result=search_engine.searchvector(query=query,k=5,score_threshold=0.6)
    result_document=[doc[0].page_content for doc in search_result]
    print(result_document)

generate_response()