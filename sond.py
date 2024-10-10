import os
import requests
from config import *
from telebot import TeleBot
import speech_recognition as sr
from pydub import AudioSegment

api_key = "3514c40a2ff64c0e9290c2fbba7a4dda"  # Your API Key
api_url = "http://api.voicerss.org/"

def handle_message(a):
    # تحقق مما إذا كان هناك رد على رسالة
    if a.reply_to_message:
        text_to_convert = a.reply_to_message.text  # النص الذي سيتم تحويله
        combined_text = f"{text_to_convert} (English: {text_to_convert}, Arabic: {text_to_convert})"  # نص مشترك

        # معالجة النص لتحويله إلى صوت
        response = requests.get(api_url + "?key=" + api_key + "&hl=ar-sa&c=MP3&src=" + text_to_convert)
        if response.status_code != 200 or len(response.content) == 0:
            bot.send_message(a.chat.id, "حدث خطأ أثناء معالجة النص.")
            return

        audio_file_name = text_to_convert[:30].replace(" ", "_")  # استبدال الفراغات لتجنب المشاكل في أسماء الملفات
        with open(f"{audio_file_name}.mp3", "wb") as audio_file:
            audio_file.write(response.content)
        if os.path.getsize(f"{audio_file_name}.mp3") == 0:
            bot.send_message(a.chat.id, "الملف الصوتي فارغ.")
            return

        # إرسال رسالة توضح أن الصوت تم تحويله
        bot.send_message(a.chat.id, "تم تحويل الرسالة إلى صوت.")

        # إرسال الملف الصوتي
        with open(f"{audio_file_name}.mp3", "rb") as audio_file:
            bot.send_voice(a.chat.id, audio_file)

    else:
        bot.send_message(a.chat.id, "يرجى الرد على رسالة لتحويلها إلى صوت.")
        
        
 
def audio_to_text(audio_file):
    # تهيئة recognizer
    r = sr.Recognizer()
    
    # تحويل الملف الصوتي إلى WAV إذا لم يكن بصيغة WAV
    if not audio_file.endswith('.wav'):
        sound = AudioSegment.from_file(audio_file)
        audio_file = audio_file.replace(audio_file.split('.')[-1], 'wav')
        sound.export(audio_file, format="wav")
    
    # فتح الملف الصوتي واستخراج النص
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    
    return text

# دالة معالجة الرسائل الصوتية التي تم الرد عليها
def handle_voice_message(a):
    # تحميل الرسالة الصوتية من الرد
    file_info = bot.get_file(a.reply_to_message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # حفظ الملف الصوتي
    with open("audio.ogg", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # تحويل الملف الصوتي إلى نص
    try:
        text = audio_to_text("audio.ogg")
        bot.reply_to(a, f"النص المستخرج: {text}")
    except Exception as e:
        bot.reply_to(a, f"حدث خطأ أثناء تحويل الصوت إلى نص: {e}")

