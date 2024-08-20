import requests
from bs4 import BeautifulSoup

url = "https://www.petofy.com/online-pet-health-record/membership-pricing"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all(class_='content-wrapper')

    for element in elements:
        for tag in element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
            print(tag.get_text(strip=True))
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
