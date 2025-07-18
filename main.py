from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

# Health check route for UptimeRobot
@app.route("/")
def home():
    return "Bot is alive!"

# Telegram bot logic
async def filter_mywin_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if (message.photo or message.video) and message.caption:
        if message.caption.lower().startswith("#mywin"):
            return  # Valid message
    await message.delete()

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def run_telegram():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.ALL, filter_mywin_media))
    app_bot.run_polling()

# Run both Flask and Telegram
if __name__ == "__main__":
    Thread(target=run_flask).start()
    Thread(target=run_telegram).start()
