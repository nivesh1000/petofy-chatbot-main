from dotenv import load_dotenv
from vector import VectorSearch
load_dotenv()
from response import Response
robj=Response()


def generate_response(query):
    search_engine=VectorSearch()
    search_result=search_engine.searchvector(query=query,k=5,score_threshold=0.1)
    similar_queries = [doc[0].page_content for doc in search_result]
    return robj.chat_completion(query,similar_queries)

def main() -> None:
    while True:   
        query=input("query>> ")
        if query=="exit":
            break
        print(f"Response>> {generate_response(query)}")

if __name__ == "__main__":
    main()        