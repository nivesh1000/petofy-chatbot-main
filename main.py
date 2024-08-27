from dotenv import load_dotenv
from vector import VectorSearch
import threading
from response import Response
from scheduler import start_scheduler
import argparse
load_dotenv()
robj=Response()


def generate_response(query):
    search_engine=VectorSearch()
    search_result=search_engine.searchvector(query=query,k=5,score_threshold=0.1)
    similar_queries = [doc[0].page_content for doc in search_result]
    return robj.chat_completion(query,similar_queries)

def main() -> None:
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

    parser = argparse.ArgumentParser(description="Interractive chat-bot which answers user query about Petofy")
    parser.add_argument('-q', '--query', type=str, help='Query to be processed', required=False)
    args = parser.parse_args()

    if args.query:
        print(args.query)
        if args.query.lower() == "exit":
            return
        print(f"Response>> {generate_response(args.query)}")
    
    while True:
        query = input("Query>> ")
        if query.lower() == "exit":
            break
        print(f"Response>> {generate_response(query)}")

if __name__ == "__main__":
    main()