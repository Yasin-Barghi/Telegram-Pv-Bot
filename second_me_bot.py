import os
import telebot
from threading import Thread
from flask import Flask

# ساخت بات
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# هندلر پیام
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, f"🔁 دریافت شد:\n{message.text}")

# تابع اجرای بات
def run_bot():
    print("🤖 Bot polling is running...")
    bot.infinity_polling()

# ساخت Flask برای پورت
app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Bot is alive!', 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# اجرای همزمان بات و سرور
if __name__ == "__main__":
    Thread(target=run_bot).start()
    run_flask()
