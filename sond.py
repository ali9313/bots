import requests
from config import *

api_key = "3514c40a2ff64c0e9290c2fbba7a4dda"  # Your API Key
api_url = "http://api.voicerss.org/"
def handle_message(a):
    # تحقق مما إذا كان هناك رد على رسالة
    if a.reply_to_message:
        text_to_convert_en = a.reply_to_message.text
        text_to_convert_ar = a.reply_to_message.text
        
        # معالجة النص الإنجليزي
        response_en = requests.get(api_url + "?key=" + api_key + "&hl=en-us&c=MP3&src=" + text_to_convert_en)
        audio_en = text_to_convert_en[:30].replace(" ", "_")  # استبدال الفراغات لتجنب المشاكل في أسماء الملفات
        with open(f"{audio_en}.mp3", "wb") as audio_file:
            audio_file.write(response_en.content)
        
        # معالجة النص العربي
        response_ar = requests.get(api_url + "?key=" + api_key + "&hl=ar-sa&c=MP3&src=" + text_to_convert_ar)
        audio_ar = text_to_convert_ar[:30].replace(" ", "_")  # استبدال الفراغات لتجنب المشاكل في أسماء الملفات
        with open(f"{audio_ar}.mp3", "wb") as audio_file:
            audio_file.write(response_ar.content)

        # إرسال رسالة توضح أن الصوت تم تحويله
        bot.send_message(a.chat.id, "تم تحويل الرسالة إلى صوت.")
    else:
        bot.send_message(a.chat.id, "يرجى الرد على رسالة لتحويلها إلى صوت.")
