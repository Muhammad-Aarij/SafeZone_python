import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_dataLahore(url):
    response = requests.get(url)
    htmlContent = response.content

    soup = BeautifulSoup(htmlContent, 'html.parser')

    lahore_div = soup.find('div', class_='tab-temp')

    lahoreLow = lahore_div.find('span', class_='tab-temp-low')['data-value']

    tr_element = soup.find('tr', class_='step-temp')

    lahoreHigh = tr_element.find('td', headers='d0Temp').div.get_text(strip=True) if tr_element and tr_element.find('td', headers='d0Temp') and tr_element.find('td', headers='d0Temp').div else None

    lahoreHigh = lahoreHigh.replace('°', '')

    lahoreHigh = int(lahoreHigh)
    
    lahoreLow = int(float(lahoreLow))

    today_date = datetime.now().date()

    span_id = f"tabSummaryText{today_date.strftime('%Y-%m-%d')}" 
    
    span_element = soup.find('div', id=span_id)

    data_inside_span = span_element.get_text(strip=True) if span_element and span_element.div else None

    return {
        'lahore High Temperature': f"{lahoreHigh}°C",
        'lahore Low Temperature': f"{lahoreLow}°C",
        'Today\'s Day': today_date.strftime('%d'),
        'Data Inside Span': data_inside_span
    }

def precipitationLahore(url):
    response = requests.get(url)
    htmlContent = response.content

    soup = BeautifulSoup(htmlContent, 'html.parser')

    tr_element = soup.find('tr', class_='step-pop')

    rain = tr_element.find('td', headers='d0PoP').get_text(strip=True) if tr_element and tr_element.find('td', headers='d0PoP') else None

    return rain

today_date = datetime.now().date()

day_of_month = today_date.strftime('%d')

url = f"https://www.metoffice.gov.uk/weather/forecast/ttsg7rxb5#?date={today_date.strftime('%Y-%m-%d')}"

scraped_data = scrape_dataLahore(url)

rain = precipitationLahore(url)

lahoreHigh = scraped_data['lahore High Temperature']
lahoreLow = scraped_data['lahore Low Temperature']
condition = scraped_data['Data Inside Span']

