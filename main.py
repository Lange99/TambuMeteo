from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update, Bot
from telegram.error import Forbidden
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          MessageHandler,
                          ContextTypes)
from telegram.ext.filters import LOCATION
import sqlite3
import os

import weatherRequest

db_name = 'locations.db'


async def update_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update['message']['chat']['id']
    lat = update['message']['location']['latitude']
    lon = update['message']['location']['longitude']
    try:
        with sqlite3.connect(db_name) as con:
            cur = con.cursor()
            query = f'INSERT OR REPLACE INTO locations VALUES \
                        ({chat_id}, {lat}, {lon})'
            cur.execute(query)
            con.commit()
            await update.message.reply_text('Position updated.')
    except Exception:
        await update.message.reply_text('Position not updated, retry later.')


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Usage: share your current position. \
        \nEvery day at 3AM UTC you'll receive a message if it will rain.")


async def send_all():
    users = []
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        users = [row for row in cur.execute('SELECT * FROM locations')]

    for user_id, lat, lon in users:
        try:
            response = weatherRequest.weather_request(lat, lon)
            if weatherRequest.will_rain(response):
                try:
                    await bot.sendMessage(user_id, 'Warning. It may rain.')
                except Forbidden:
                    with sqlite3.connect(db_name) as con:
                        cur = con.cursor()
                        cur.execute(
                            f'DELETE FROM locations WHERE chat_id={user_id}'
                        )
                        con.commit()
        except Exception:
            await bot.sendMessage(user_id, 'Warning! Weather service out.')


sched = AsyncIOScheduler(timezone="UTC")
sched.add_job(send_all, 'cron', hour=3)
sched.start()

telegram_token = os.environ['TELEGRAM_TOKEN']
bot = Bot(telegram_token)
app = ApplicationBuilder().token(telegram_token).build()
app.add_handler(CommandHandler('start', helper))
app.add_handler(MessageHandler(LOCATION, update_location))
app.run_polling()
