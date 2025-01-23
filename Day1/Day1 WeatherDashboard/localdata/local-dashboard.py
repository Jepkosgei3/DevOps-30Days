import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('OPEN_WEATHER_API_KEY')  # Fetch the API key from the environment
CITIES = ['Nairobi', 'Arusha', 'Kampala']
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def main():
    weather_data = {}
    for city in CITIES:
        data = fetch_weather_data(city)
        weather_data[city] = data

    # Save the data to a local JSON file
    with open('weather_data.json', 'w') as f:
        json.dump(weather_data, f, indent=4)

if __name__ == '__main__':
    main()