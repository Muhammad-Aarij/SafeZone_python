from bs4 import BeautifulSoup
import requests
import re

def scrape_imageofRainfall_sources():
    url = "https://ndmc.pmd.gov.pk/new/outlooks.php?p=rainfall-analysis"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        img_tags = soup.find_all('img', class_='img-responsive', src=re.compile(r'/assets'))

        img_sources = [img.get('src') for img in img_tags]

        return img_sources
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
