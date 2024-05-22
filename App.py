from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import openai

from weatherIslamabad import scrape_dataIslamabad, precipitationIslamabad
from weatherkarachi import scrape_dataKarachi, precipitationKarachi
from weatherlahore import scrape_dataLahore, precipitationLahore
from weathergilgit import scrape_dataGilgit, precipitationGilgit
from weatherQuetta import scrape_dataQuetta, precipitationQuetta
from weatherpeshawar import scrape_dataPeshawar, precipitationPeshawar
from weathertable import scrape_weekly_outlook
from earthquakeUpdates import scrape_seismic_data1
from Seismic import scrape_seismicity_maps
from disasterNews import scrape_news
from Weather_Climate import scrape_weather_data
from WaterResorvior import scrape_imageofwater_resorvior_sources
from Motorway import scrape_motorway_data
from Dought_rainfall_images import scrape_imageofRainfall_sources


app = Flask(__name__)
CORS(app)  

openai.api_key = 'sk-proj-7Lv0uHPJj2CaBuX9Be83T3BlbkFJne3b2rF7A8n9pB93XfW9'


def get_city_weather(city, cityname, scrape_function, precipitation_function):
    url = f"https://www.metoffice.gov.uk/weather/forecast/{city}#?date={today_date.strftime('%Y-%m-%d')}"
    scraped_data = scrape_function(url)
    rain = precipitation_function(url)

    high_key = f'{cityname} High Temperature'
    low_key = f'{cityname} Low Temperature'

    return {
        'cityName': cityname,
        'high': scraped_data.get(high_key, None),
        'low': scraped_data.get(low_key, None),
        'rain': rain,
        'condition': scraped_data.get('Data Inside Span', None)
    }

today_date = datetime.now().date()

 
day_of_month = today_date.strftime('%d')

@app.route('/weather/all', methods=['GET'])
def get_all_weather():
    cities = [
        ('ttgzybxnz', 'islamabad', scrape_dataIslamabad, precipitationIslamabad),
        ('tkrtt71fb', 'karachi', scrape_dataKarachi, precipitationKarachi),
        ('ttsg7rxb5', 'lahore', scrape_dataLahore, precipitationLahore),
        ('twku77j3n', 'gilgit', scrape_dataGilgit, precipitationGilgit),
        ('tmrs4y3xt', 'quetta', scrape_dataQuetta, precipitationQuetta),
        ('tw51sgs68', 'peshawar', scrape_dataPeshawar, precipitationPeshawar)
    ]

    all_data = []

    for city in cities:
        city_data = get_city_weather(*city)
        all_data.append(city_data)

    return jsonify(all_data)

@app.route('/news', methods=['GET'])
def get_news():
    news_data = scrape_news()
    return jsonify(news_data)

@app.route('/weather/scrapeClimate', methods=['GET'])
def scrape_weather_route():
    scraped_data = scrape_weather_data()
    return jsonify(scraped_data)

@app.route('/weather/scrape_weekly_outlook', methods=['GET'])
def scrape_weeklyweather_route():
    scraped_data = scrape_weekly_outlook()
    return jsonify(scraped_data)    

@app.route('/weather/eathquaketable1', methods=['GET'])
def scrape_earthquake_table1():
    scraped_data = scrape_seismic_data1()
    return jsonify(scraped_data)

@app.route('/weather/eathquaketable2', methods=['GET'])
def scrape_earthquake_table2():
    scraped_data = scrape_seismicity_maps()
    return jsonify(scraped_data)

@app.route('/weather/waterresorvior', methods=['GET'])
def scrape_water_Resorvior():
    scraped_data = scrape_imageofwater_resorvior_sources()
    return jsonify(scraped_data)

@app.route('/weather/rainanalysis', methods=['GET'])
def scrape_water_Analysis():
    scraped_data = scrape_imageofRainfall_sources()
    return jsonify(scraped_data)

@app.route('/weather/motorwaysmog', methods=['GET'])
def scrape_Smog_Analysis():
    scraped_data = scrape_motorway_data()
    return jsonify(scraped_data)

@app.route('/message', methods=['POST'])
def handle_message():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        bot_message = response.choices[0].message['content']
        return jsonify({"message": bot_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000) 