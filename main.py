from webscrape import webscrape
import os
from chroma import Chromaappender
from response import Response
from pydantics import UserModel, ValidationError
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
dbloc = os.getenv("DB_LOC")
scrapedataloc = os.getenv("SCRAPE_DATA_LOC")
urls = [
    "https://www.petofy.com/online-pet-health-record/membership-pricing",
    "https://petofy.com/pet-microchip-registry",
    "https://petofy.com/VetOnCall"
]

os.environ["TOKENIZERS_PARALLELISM"] = os.getenv("TOKENIZERS_PARALLELISM")

webscrape(scrapedataloc, urls)

cobj = Chromaappender(db_name, dbloc, scrapedataloc)
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
    while(True):
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
                similar_results = cobj.similarity_search(user_query)
                response = robj.chat_completion(user_query, similar_results)
                print(f"Response>> {response}")
        except ValidationError as e:
            print(f"Validation error: {e}")

if __name__ == "__main__":
    main()
