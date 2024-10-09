import os
import requests
from config import *
from telebot import TeleBot

api_key = "3514c40a2ff64c0e9290c2fbba7a4dda"  # Your API Key
api_url = "http://api.voicerss.org/"
def handle_message(a):
    # تحقق مما إذا كان هناك رد على رسالة
    if a.reply_to_message:
        text_to_convert_en = a.reply_to_message.text
        text_to_convert_ar = a.reply_to_message.text
        
        # معالجة النص الإنجليزي
        response_en = requests.get(api_url + "?key=" + api_key + "&hl=en-us&c=MP3&src=" + text_to_convert_en)
        if response_en.status_code != 200 or len(response_en.content) == 0:
            bot.send_message(a.chat.id, "حدث خطأ أثناء معالجة النص الإنجليزي.")
            return
        
        audio_en = text_to_convert_en[:30].replace(" ", "_")  # استبدال الفراغات لتجنب المشاكل في أسماء الملفات
        with open(f"{audio_en}.mp3", "wb") as audio_file:
            audio_file.write(response_en.content)
        if os.path.getsize(f"{audio_en}.mp3") == 0:
            bot.send_message(a.chat.id, "الملف الصوتي الإنجليزي فارغ.")
            return

        # معالجة النص العربي
        response_ar = requests.get(api_url + "?key=" + api_key + "&hl=ar-sa&c=MP3&src=" + text_to_convert_ar)
        if response_ar.status_code != 200 or len(response_ar.content) == 0:
            bot.send_message(a.chat.id, "حدث خطأ أثناء معالجة النص العربي.")
            return
        
        audio_ar = text_to_convert_ar[:30].replace(" ", "_")  # استبدال الفراغات لتجنب المشاكل في أسماء الملفات
        with open(f"{audio_ar}.mp3", "wb") as audio_file:
            audio_file.write(response_ar.content)
        if os.path.getsize(f"{audio_ar}.mp3") == 0:
            bot.send_message(a.chat.id, "الملف الصوتي العربي فارغ.")
            return

        # إرسال رسالة توضح أن الصوت تم تحويله
        bot.send_message(a.chat.id, "تم تحويل الرسالة إلى صوت.")

        # إرسال الملفات الصوتية
        with open(f"{audio_en}.mp3", "rb") as audio_file_en:
            bot.send_voice(a.chat.id, audio_file_en)

        with open(f"{audio_ar}.mp3", "rb") as audio_file_ar:
            bot.send_voice(a.chat.id, audio_file_ar)

    else:
        bot.send_message(a.chat.id, "يرجى الرد على رسالة لتحويلها إلى صوت.")