import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import os
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6756150197  # آی‌دی عددی خودت رو بذار اینجا

bot = telebot.TeleBot(TOKEN)

# برای ذخیره‌سازی اینکه ادمین قراره به کی جواب بده
admin_target = {
    'mode': None,  # 'reply' یا 'direct'
    'user_id': None,
    'reply_to': None
}

# 📥 کاربر پیام می‌فرسته → می‌ره برای ادمین
@bot.message_handler(func=lambda m: m.chat.type == 'private' and m.from_user.id != ADMIN_ID,
                     content_types=['text', 'photo', 'voice', 'video', 'document', 'audio', 'sticker', 'animation', 'video_note'])
def handle_user_message(message):
    user = message.from_user
    caption = message.caption or ''
    text = message.text or ''
    content = caption or text or '📎 پیام جدید'

    # دکمه‌ها
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("✉️ پاسخ مستقیم", callback_data=f"direct_{user.id}"),
        InlineKeyboardButton("🔁 ریپلای به این پیام", callback_data=f"reply_{user.id}_{message.message_id}")
    )

    # ارسال به ادمین با توجه به نوع پیام
    if message.content_type == 'text':
        bot.send_message(ADMIN_ID, f"📨 از {user.first_name}:\n\n{text}", reply_markup=keyboard)
    elif message.content_type == 'photo':
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"📸 از {user.first_name}:\n\n{caption}", reply_markup=keyboard)
    elif message.content_type == 'voice':
        bot.send_voice(ADMIN_ID, message.voice.file_id, caption=f"🎤 از {user.first_name}:", reply_markup=keyboard)
    elif message.content_type == 'video':
        bot.send_video(ADMIN_ID, message.video.file_id, caption=f"🎞️ از {user.first_name}:\n\n{caption}", reply_markup=keyboard)
    elif message.content_type == 'document':
        bot.send_document(ADMIN_ID, message.document.file_id, caption=f"📎 از {user.first_name}:\n\n{caption}", reply_markup=keyboard)
    elif message.content_type == 'audio':
        bot.send_audio(ADMIN_ID, message.audio.file_id, caption=f"🎵 از {user.first_name}:\n\n{caption}", reply_markup=keyboard)
    elif message.content_type == 'sticker':
        bot.send_sticker(ADMIN_ID, message.sticker.file_id, reply_markup=keyboard)
    elif message.content_type == 'animation':
        bot.send_animation(ADMIN_ID, message.animation.file_id, caption=f"🎞️ گیف از {user.first_name}:", reply_markup=keyboard)
    elif message.content_type == 'video_note':
        bot.send_video_note(ADMIN_ID, message.video_note.file_id, reply_markup=keyboard)

# 📌 ادمین یکی از دکمه‌ها رو می‌زنه
@bot.callback_query_handler(func=lambda call: call.data.startswith(('reply_', 'direct_')))
def callback_handler(call):
    global admin_target
    data = call.data

    if data.startswith('reply_'):
        _, user_id, reply_to = data.split('_')
        admin_target = {'mode': 'reply', 'user_id': int(user_id), 'reply_to': int(reply_to)}
        bot.answer_callback_query(call.id, "🔁 حالت ریپلای فعال شد")
        bot.send_message(ADMIN_ID, f"🔁 حالا پیام بفرست تا به پیام کاربر {user_id} ریپلای بشه.")

    elif data.startswith('direct_'):
        _, user_id = data.split('_')
        admin_target = {'mode': 'direct', 'user_id': int(user_id), 'reply_to': None}
        bot.answer_callback_query(call.id, "✉️ حالت پیام مستقیم فعال شد")
        bot.send_message(ADMIN_ID, f"✉️ حالا پیام بفرست تا مستقیماً برای کاربر {user_id} ارسال بشه.")

# 📨 ادمین پیام می‌فرسته
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID,
                     content_types=['text', 'photo', 'voice', 'video', 'document', 'audio', 'sticker', 'animation', 'video_note'])
def handle_admin_send(message):
    if admin_target['user_id'] is None:
        bot.send_message(ADMIN_ID, "⚠️ لطفاً اول یکی از دکمه‌های زیر پیام کاربران رو بزن.")
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

# ▶️ اجرا
print("🤖 Bot is running...")
bot.infinity_polling()
