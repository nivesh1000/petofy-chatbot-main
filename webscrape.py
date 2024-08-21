import requests
from bs4 import BeautifulSoup

def webscrape(file_path, urls):
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(f"----Content from {url}---- \n")
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                elements = soup.find(class_='content-wrapper')
                tags = elements.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'label'])
                for tag in tags:
                    file.write(tag.get_text(strip=True) + '\n')
                file.write('\n')
            else:
                file.write(f"Failed to retrieve the webpage {url}. Status code: {response.status_code}\n")

    print("Scraping completed and data has been written to 'crawled_data.txt'.")
