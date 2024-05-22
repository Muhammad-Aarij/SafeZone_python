import requests
from bs4 import BeautifulSoup
import re

def scrape_imageofwater_resorvior_sources():
    url = "https://ndmc.pmd.gov.pk/new/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        img_tags = soup.find_all('img', src=re.compile(r'/assets'))

        img_sources = []
        for img in img_tags[-3:]:
            img_sources.append(img.get('src'))

        return img_sources
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

