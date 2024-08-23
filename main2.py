from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from vector2 import BeckHealthVectorSearch
load_dotenv()
from response import Response
robj=Response()

def chat_completion(self, user_query, similarity_result):
    with open('system_prompt.txt', 'r') as file:
        base_prompt = file.read()
    deployment = os.getenv("DEPLOYEMENT")

    final_prompt = base_prompt.format(
        similarity_result=similarity_result,
        user_query=user_query
    )
    completion = self.client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "user", "content": final_prompt},
        ],
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    return completion.choices[0].message.content

# completion()

def generate_response(query):
    search_engine=BeckHealthVectorSearch()
    search_result=search_engine.searchvector(query=query,k=5,score_threshold=0.1)
    similar_queries = [doc[0].page_content for doc in search_result]
    return robj.chat_completion(query,similar_queries)
    
query=input("query>> ")
print(f"Response>> {generate_response(query)}")