from bs4 import BeautifulSoup
import requests

def scrape_weekly_outlook():
    weekly_outlook_url = "https://nwfc.pmd.gov.pk/new/weekly-outlook-en.php"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(weekly_outlook_url, headers=headers)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='table-bordered')

        if table:

            rows = table.select('tbody tr')


            data_list = []

            for row in rows:

                cells = row.find_all(['td', 'th'])
                
                date_parts = cells[0].text.strip().split(',')
                date = date_parts[0].strip()
                day = date_parts[1].strip()

                row_data = {'Date': date, 'Day': day, 'Weather_Outlook': cells[1].text.strip()}


                data_list.append(row_data)

            return data_list

    return None


weekly_outlook_data = scrape_weekly_outlook()

