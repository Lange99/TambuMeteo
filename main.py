import time
import telepot
import os

import weatherRequest

# simple reply bot


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    weatherRequest.weather_request(msg['text'])
    print(command)
    bot.sendMessage(chat_id, command)


telegram_token = os.environ["TELEGRAM_TOKEN"]
bot = telepot.Bot(telegram_token)
# weatherRequest.weather_request("brescia")
bot.message_loop(handle)
while True:
    time.sleep(10)