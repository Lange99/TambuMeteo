from apscheduler.schedulers.blocking import BlockingScheduler

import weatherRequest
import telepot
import os

# simple reply bot
users = {}


def handle(msg):
    global users
    chat_id = msg['chat']['id']

    if msg.get('location'):
        users[chat_id] = msg['location']
        print(msg['location'])
        bot.sendMessage(chat_id, "Position saved")


def send_all():
    for user_id, location in users.items():
        response = weatherRequest.weather_request(
            location['latitude'], location['longitude']
        )

        if weatherRequest.will_rain(response):
            bot.sendMessage(user_id, "Warning. It may rain.")


telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telepot.Bot(telegram_token)
bot.message_loop(handle)

sched = BlockingScheduler()
sched.add_job(send_all, 'cron', hour=3)
sched.start()
