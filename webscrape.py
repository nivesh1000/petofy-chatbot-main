import requests
from bs4 import BeautifulSoup
import os

class WebScrape:
    def __init__(self,sitemap_url,sloc) -> None:
        self.sitemap_url=sitemap_url
        self.sloc=sloc
        self.scrapewriter()

    
    def scrapewriter(self):
        urls = self.get_sitemap_urls()
        all_text = ""
        with open(self.sloc, 'a', encoding='utf-8') as file:
            for url in urls:
                print(f"Crawling {url}")
                page_text = self.crawl_page(url)
                all_text = f"\n\n--- Content from {url} ---\n\n" + page_text
                file.write(all_text)

    def get_sitemap_urls(self):
        response = requests.get(self.sitemap_url)
        soup = BeautifulSoup(response.content, 'lxml')
        urls = [loc.text for loc in soup.find_all('loc')]
        return urls  

    def crawl_page(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        return self.extract_main_content(soup)          
        
    def extract_main_content(self,soup):
        main_content = []
        
        # Tags that often contain main content
        tags = ['p', 'div', 'article', 'section']

        for tag in tags:
            for element in soup.find_all(tag):
                text = element.get_text(strip=True)
                if text:  # Ensure the text is not empty
                    main_content.append(text)
        
        # Join all extracted text parts with a newline
        return '\n'.join(main_content)    
    
