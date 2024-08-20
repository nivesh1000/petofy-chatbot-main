import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.petofy.com/online-pet-health-record/membership-pricing",
    "https://petofy.com/pet-microchip-registry",
    "https://petofy.com/VetOnCall"
]
file_path= "/home/oem/Documents/petofy-chatbot-main/staticdata/crawled_data.txt"
with open(file_path, 'w') as file:
    for url in urls:
        file.write(f"----Content from {url}---- \n")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all(class_='content-wrapper')

            for element in elements:
                for tag in element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'label']):
                    file.write(tag.get_text(strip=True) + '\n')
            file.write('\n')
        else:
            file.write(f"Failed to retrieve the webpage {url}. Status code: {response.status_code}\n")

print("Scraping completed and data has been written to 'crawled_data.txt'.")
