import requests
from bs4 import BeautifulSoup

def scrape_seismicity_maps():
    url="https://seismic.pmd.gov.pk/seismicity-maps.php"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='table')

        if table:
            rows = table.select('tbody tr')

            data_list = []

            for row in rows:
                cells = row.find_all('td')
                row_data = {'Date': cells[0].text.strip(), 'Map_URL': cells[1].find('a')['href']}

                data_list.append(row_data)

            return data_list
        else:
            print("Table not found on the webpage.")
            return None
    else:
        print("Failed to retrieve the webpage. Check the URL.")
        return None

