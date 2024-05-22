import requests
from bs4 import BeautifulSoup

def scrape_seismic_data1():
    url = "https://seismic.pmd.gov.pk/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.select('tbody tr')

        scraped_data = []

        for row in rows:
            cells = row.find_all('td')
            date = cells[0].text.strip()
            time_utc = cells[1].text.strip()
            region = cells[2].text.strip()
            magnitude = cells[3].text.strip()
            depth = cells[4].text.strip()
            mode = cells[7].text.strip()

            mode = 'Strong' if mode == 'A' else 'Moderate'

            entry = {
                'Date': date,
                'Time': time_utc,
                'Region': region,
                'Magnitude': magnitude,
                'Depth': depth,
                'Mode': mode,
            }

            scraped_data.append(entry)

        return scraped_data
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

