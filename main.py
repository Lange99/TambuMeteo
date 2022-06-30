import time
import telepot
import os

import weatherRequest

# simple reply bot
users = {}

def handle(msg):
    global users
    chat_id = msg['chat']['id']

    if msg.get('location'):
        users[chat_id] = msg['location']
        lat = msg['location']['latitude']
        lon = msg['location']['longitude']
        weather = weatherRequest.weather_request(lat, lon)
        print(weather)
        bot.sendMessage(chat_id, "poition saved")
    else:
        pass
        #print hello world and user guide
        #print(command)
        #city = command.split(' ')[1]
        #response = weatherRequest.weather_request(city)
        #print(response)
        bot.sendMessage(chat_id, "hello world and user guide")


telegram_token = os.environ["TELEGRAM_TOKEN"]
bot = telepot.Bot(telegram_token)
# weatherRequest.weather_request("brescia")
bot.message_loop(handle)
while True:
    time.sleep(10)