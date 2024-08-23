from webscrape import webscrape
import schedule
import os
import datetime
from dotenv import load_dotenv
import time
from chroma import Chromaappender
import shutil

load_dotenv()

scrapedataloc = os.getenv("SCRAPE_DATA_LOC")
urls = [
    "https://www.petofy.com/online-pet-health-record/membership-pricing",
    "https://petofy.com/pet-microchip-registry",
    "https://petofy.com/VetOnCall"
]
db_name = os.getenv("DB_NAME")
dbloc = os.getenv("DB_LOC")


def initialize_chromaappender():
    if os.path.exists(dbloc):
        shutil.rmtree(dbloc)
    os.makedirs(dbloc)
    print(f"{dbloc} folder deleted and recreated.")
    webscrape(scrapedataloc, urls)
    print(f"Scraping and appending run completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return Chromaappender(db_name, dbloc, scrapedataloc)


def start_scheduler():
    schedule.every(6).minutes.do(initialize_chromaappender)
    while True:
        schedule.run_pending()
        time.sleep(1)
