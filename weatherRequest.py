from datetime import datetime
import requests
import os


def weather_request(lat, lon):
    api_url = "http://api.openweathermap.org/data/2.5/forecast?lat="
    appid = os.environ["OPENWEATHER_APPID"]
    url = api_url + str(lat) + "&lon=" + str(lon) + "&appid=" + appid
    response = requests.get(url)
    data = response.json()
    return data


def will_rain(data, threshold=0.75):
    weathers = data["list"]
    today = datetime.today().date()
    for weather in weathers:
        weather_date = datetime.fromtimestamp(weather["dt"]).date()
        if weather_date == today:
            if weather["pop"] > threshold:
                return True

    return False
