from webscrape import webscrape
import schedule
import os
import datetime
from dotenv import load_dotenv
import time
import shutil
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from index import create_index, upload_to_index

load_dotenv()

scrapedataloc = os.getenv("SCRAPE_DATA_LOC")
urls = [
    "https://www.petofy.com/online-pet-health-record/membership-pricing",
    "https://petofy.com/pet-microchip-registry",
    "https://petofy.com/VetOnCall"
]
db_name = os.getenv("DB_NAME")
dbloc = os.getenv("DB_LOC")
service_endpoint = os.getenv("SERVICE_ENDPOINT")
index_name = "petofy-vector-data"
key = os.getenv("RESOURCE_KEY")


def delete_existing_index():
    credential = AzureKeyCredential(key)
    index_client = SearchIndexClient(endpoint=service_endpoint, credential=credential)
    try:
        index_client.delete_index(index_name)
        print(f"Deleted existing index: {index_name}")
    except Exception as e:
        print(f"Could not delete index {index_name}: {e}")
    finally:
        index_client.close()


def initialize_vectorization():
    webscrape(scrapedataloc, urls)
    print(f"Scraping completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    delete_existing_index()
    create_index()
    upload_to_index()



def start_scheduler():
    schedule.every(2).minutes.do(initialize_vectorization)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_scheduler()
