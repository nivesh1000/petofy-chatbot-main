# main.py
from schedular import initialize_chromaappender, start_scheduler
from response import Response
from pydantics import UserModel, ValidationError
import os
from dotenv import load_dotenv
import threading
import time

load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = os.getenv("TOKENIZERS_PARALLELISM")

cobj = initialize_chromaappender()
robj = Response()

code_index = {
    '100': "User query cannot be empty.",
    '101': "User query cannot be only digits. Please ask a valid question.",
    '102': "Certain invalid symbols are identified in the user query. Please ask a query without them.",
    '103': "User Query must contain at least one English alphabet [a-z, A-Z]",
    '200': "Your Query is identified as hate speech. Please ask a valid question.",
    '201': "Severity level too high for hate speech.",
    '300': "User query identified as promoting self-harm. Please ask an appropriate question.",
    '301': "Severity level too high for self-harm.",
    '400': "User query identified as inappropriate or explicit sexual material. Please ask an appropriate question.",
    '401': "Severity level too high for sexual content.",
    '500': "User query identified as promoting violence. Please ask an appropriate question.",
    '501': "Severity level too high for violent content.",
}

def main() -> None:
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

    while True:
        user_query = input("Query>> ")
        if user_query == 'exit':
            break
        try:
            code = UserModel(user_query=user_query)
            code = str(code)
            code = code[len(code)-5:len(code)]
            code = code[1:len(code)-1]
            if code in code_index:
                print(f"Response>> {code_index[code]}")
            else:
                if cobj is not None:
                    similar_results = cobj.similarity_search(user_query)
                    response = robj.chat_completion(user_query, similar_results)
                    print(f"Response>> {response}")
                else:
                    print("Response>> Chromaappender is not initialized yet.")
        except ValidationError as e:
            print(f"Validation error: {e}")

if __name__ == "__main__":
    main()
