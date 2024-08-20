from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class Response:
    def __init__(self) -> None:
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        ) 

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
