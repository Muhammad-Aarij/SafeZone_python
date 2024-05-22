import requests
from bs4 import BeautifulSoup

def scrape_weather_data():
    url = "https://nwfc.pmd.gov.pk/new/daily-forecast-en.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        printable_area_div = soup.find('div', id='printableArea')

        col_md_12_divs = printable_area_div.find_all('div', class_='col-md-12')

        if len(col_md_12_divs) >= 2:
            weather_div = col_md_12_divs[1]

            h5_tags = weather_div.find_all('h5')
            p_tags = weather_div.find_all('p')

            weather_data_array = []

            for h5_tag, p_tag in zip(h5_tags, p_tags):
                heading = h5_tag.text.strip()
                detail = p_tag.text.strip()
                row_data = {'Heading': heading, 'Detail': detail}
                weather_data_array.append(row_data)

            return weather_data_array
        else:
            print("No second div with class 'col-md-12' found inside the div with id 'printableArea'")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return None

