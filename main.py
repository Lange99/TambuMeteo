from apscheduler.schedulers.blocking import BlockingScheduler
import telepot
import sqlite3
import os

import weatherRequest

db_name = 'locations.db'


def handle(msg):
    chat_id = msg['chat']['id']

    if msg.get('location'):
        lat = msg['location']['latitude']
        lon = msg['location']['longitude']
        try:
            with sqlite3.connect(db_name) as con:
                cur = con.cursor()
                query = f"""INSERT INTO locations VALUES
                            ({chat_id}, {lat}, {lon})"""
                cur.execute(query)
                con.commit()
                bot.sendMessage(chat_id, "Position updated.")
        except Exception:
            bot.sendMessage(chat_id, "Position not updated, retry later.")


def send_all():
    users = []
    with sqlite3.connect() as con:
        cur = con.cursor()
        users = [row for row in cur.execute('SELECT * FROM locations')]

    for user_id, lat, lon in users:
        try:
            response = weatherRequest.weather_request(lat, lon)
            if weatherRequest.will_rain(response):
                bot.sendMessage(user_id, "Warning. It may rain.")
        except Exception:
            bot.sendMessage(user_id, "Check manually. Weather service out")


telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telepot.Bot(telegram_token)
bot.message_loop(handle)

sched = BlockingScheduler()
sched.add_job(send_all, 'cron', hour=3)
sched.start()
