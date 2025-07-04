import os
import telebot
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توکن و آیدی ادمین از متغیر محیطی
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)

# وضعیت هدف پیام‌ها
admin_target = {
    'mode': None,  # 'reply' یا 'direct'
    'user_id': None,
    'reply_to': None
}

# هندل پیام از کاربران (غیر از ادمین)
@bot.message_handler(func=lambda m: m.chat.type == 'private' and m.from_user.id != ADMIN_ID,
                     content_types=['text', 'photo', 'voice', 'video', 'document', 'audio', 'sticker', 'animation', 'video_note'])
def handle_user_message(message):
    user = message.from_user
    caption = message.caption or ''
    text = message.text or ''
    content = caption or text or '📎 پیام جدید'

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("✉️ پیام مستقیم", callback_data=f"direct_{user.id}"),
        InlineKeyboardButton("🔁 ریپلای به این پیام", callback_data=f"reply_{user.id}_{message.message_id}")
    )

    sender_info = f"از {user.first_name} (@" + (user.username or "ندارد") + ")"

    if message.content_type == 'text':
        bot.send_message(ADMIN_ID, f"📨 {sender_info}:\n\n{text}", reply_markup=keyboard)
    elif message.content_type == 'photo':
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"📸 {sender_info}:\n\n{caption}", reply_markup=keyboard)
    elif message.content_type == 'voice':
        bot.send_voice(ADMIN_ID, message.voice.file_id, caption=f"🎤 {sender_info}:", reply_markup=keyboard)
    elif message.content_type == 'video':
        bot.send_video(ADMIN_ID, message.video.file_id, caption=f"🎞️ {sender_info}:\n\n{caption}", reply_markup=keyboard)
    elif message.content_type == 'document':
        bot.send_document(ADMIN_ID, message.document.file_id, caption=f"📎 {sender_info}:\n\n{caption}", reply_markup=keyboard)
    elif message.content_type == 'audio':
        bot.send_audio(ADMIN_ID, message.audio.file_id, caption=f"🎵 {sender_info}:\n\n{caption}", reply_markup=keyboard)
    elif message.content_type == 'sticker':
        bot.send_sticker(ADMIN_ID, message.sticker.file_id, reply_markup=keyboard)
    elif message.content_type == 'animation':
        bot.send_animation(ADMIN_ID, message.animation.file_id, caption=f"🎞️ گیف {sender_info}:", reply_markup=keyboard)
    elif message.content_type == 'video_note':
        bot.send_video_note(ADMIN_ID, message.video_note.file_id, reply_markup=keyboard)

# هندل دکمه‌های ادمین
@bot.callback_query_handler(func=lambda call: call.data.startswith(('reply_', 'direct_')))
def callback_handler(call):
    global admin_target
    try:
        if call.data.startswith('reply_'):
            _, user_id, reply_to = call.data.split('_')
            admin_target = {'mode': 'reply', 'user_id': int(user_id), 'reply_to': int(reply_to)}
            bot.answer_callback_query(call.id, "🔁 حالت ریپلای فعال شد")
            bot.send_message(ADMIN_ID, f"🔁 حالا پیام بفرست تا به پیام کاربر ارسال بشه.")

        elif call.data.startswith('direct_'):
            _, user_id = call.data.split('_')
            admin_target = {'mode': 'direct', 'user_id': int(user_id), 'reply_to': None}
            bot.answer_callback_query(call.id, "✉️ حالت پیام مستقیم فعال شد")
            bot.send_message(ADMIN_ID, f"✉️ حالا پیام بفرست تا مستقیماً برای کاربر ارسال بشه.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ خطا در فعال‌سازی دکمه: {e}")

# پیام‌های ادمین برای کاربر
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID,
                     content_types=['text', 'photo', 'voice', 'video', 'document', 'audio', 'sticker', 'animation', 'video_note'])
def handle_admin_send(message):
    if admin_target['user_id'] is None:
        bot.send_message(ADMIN_ID, "⚠️ لطفاً یکی از دکمه‌های پاسخ رو بزن.")
        return

    user_id = admin_target['user_id']
    reply_to = admin_target['reply_to'] if admin_target['mode'] == 'reply' else None

    try:
        if message.content_type == 'text':
            bot.send_message(user_id, message.text, reply_to_message_id=reply_to)
        elif message.content_type == 'photo':
            bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption or "", reply_to_message_id=reply_to)
        elif message.content_type == 'voice':
            bot.send_voice(user_id, message.voice.file_id, caption=message.caption or "", reply_to_message_id=reply_to)
        elif message.content_type == 'video':
            bot.send_video(user_id, message.video.file_id, caption=message.caption or "", reply_to_message_id=reply_to)
        elif message.content_type == 'document':
            bot.send_document(user_id, message.document.file_id, caption=message.caption or "", reply_to_message_id=reply_to)
        elif message.content_type == 'audio':
            bot.send_audio(user_id, message.audio.file_id, caption=message.caption or "", reply_to_message_id=reply_to)
        elif message.content_type == 'sticker':
            bot.send_sticker(user_id, message.sticker.file_id, reply_to_message_id=reply_to)
        elif message.content_type == 'animation':
            bot.send_animation(user_id, message.animation.file_id, caption=message.caption or "", reply_to_message_id=reply_to)
        elif message.content_type == 'video_note':
            bot.send_video_note(user_id, message.video_note.file_id, reply_to_message_id=reply_to)

        bot.send_message(ADMIN_ID, "✅ پیام ارسال شد.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ خطا در ارسال پیام:\n{e}")

# سرویس Flask برای جلوگیری از خاموش شدن Render
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "✅ Bot is alive."

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# اجرای Flask در ترد جدا
Thread(target=run_flask).start()

# اجرای بات
print("🤖 Bot polling is running...")
bot.infinity_polling()
