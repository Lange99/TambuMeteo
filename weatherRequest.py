import requests
import json
import os

def weather_request(city):
    appid = os.environ["OPENWEATHER_APPID"]
    url = "http://api.openweathermap.org/data/2.5/forecast?q=" + city +"&appid=" + appid
    response = requests.get(url)
    data = response.json()
    print(data)
    return data
