import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, f"🔁 دریافت شد:\n{message.text}")

print("🤖 Bot is running...")
bot.infinity_polling()
