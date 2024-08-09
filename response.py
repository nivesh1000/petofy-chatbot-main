from openai import AzureOpenAI



class Response:
    def __init__(self) -> None:
        self.client = AzureOpenAI(
        api_key="b614b5b86d9e4baba98dbc28b802ed26",
        api_version="2024-02-01",
        azure_endpoint="https://petofy-openai.openai.azure.com/") 

    def chat_completion(self,user_query,similarity_result):
        with open('system_prompt.txt', 'r') as file:
            base_prompt = file.read()   

        deployment = "gpt-35-turbo"

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
    
