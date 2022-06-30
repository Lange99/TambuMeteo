from datetime import datetime
import requests
import json
import os

def weather_request(lat, lon):
    appid = os.environ["OPENWEATHER_APPID"]
    url = "http://api.openweathermap.org/data/2.5/forecast?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + appid
    response = requests.get(url)
    data = response.json()
    return data

def parse_weather(data):
    weathers = data["list"]
    today = datetime.today().date()
    for weather in weathers:
        weather_date = datetime.fromtimestamp(weather["dt"]).date()
        if weather_date == today:
            #