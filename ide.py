import logging
import requests
import asyncio
from config import *
from telebot import TeleBot
from telebot.types import Message
from telethon import TelegramClient

# إعداد logging لتسجيل الأخطاء في ملف log.txt
logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# إعداد Telethon client
api_id = "1747534"  # ضع هنا API ID الخاص بك
api_hash = "5a2684512006853f2e48aca9652d83ea"  # ضع هنا API Hash الخاص بك
client = TelegramClient('session_name', api_id, api_hash)

# دالة لحساب عدد الرسائل الخاصة بالمستخدم باستخدام Telethon
async def get_message_count(user_id, chat_id):
    async with client:
        zmsg = await client.get_messages(chat_id, from_user=user_id)
        return len(zmsg)

# دالة لجلب معلومات المستخدم (تكون غير متزامنة)
async def fetch_info_async(a: Message):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
        user_id = user.id
        username = f"@{user.username}" if user.username else "لا يـوجـد"
        
        # جلب معلومات البايو باستخدام get_chat
        user_chat = bot.get_chat(user_id)
        user_bio = user_chat.bio if user_chat.bio else "لا يـوجـد"
        
        # جلب عدد الرسائل الفعلي باستخدام Telethon
        zzz = await get_message_count(user_id, a.chat.id)
        
        ZED_TEXT = "المختصر  انتِ شي حلو محد يشبهه💕 🫶"
        ZEDM = "✦ "
        
        caption = f"<b>{ZED_TEXT} </b>\n"
        caption += f"<b>{ZEDM}الاســم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>"
        caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
        caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{ZEDM}الرتبــه    ⤎ العضو 𓅫 </b>\n"
        caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz} 💌\n"
        caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
        
        return caption
    except Exception as e:
        logging.error("Error in fetch_info function: %s", e)
        return "حدث خطأ أثناء جلب معلومات المستخدم."

# دالة لجلب معلومات المستخدم (تقوم بتشغيل الدالة غير المتزامنة)
def fetch_info(a: Message):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_info_async(a))
    return result

# دالة لإرسال صورة الملف الشخصي مع الكابشن
async def send_user_info_with_photo_async(a: Message):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        user_id = user.id
        
        # جلب صورة الملف الشخصي للمستخدم
        photos = bot.get_user_profile_photos(user_id)
        
        # التحقق من وجود صور للمستخدم
        if photos.total_count > 0:
            # جلب أول صورة من الصور المتاحة
            photo_file_id = photos.photos[0][-1].file_id  # جلب أعلى جودة للصورة
            
            # جلب الكابشن (المعلومات) 
            caption = await fetch_info_async(a)
            
            # إرسال الصورة مع الكابشن
            bot.send_photo(a.chat.id, photo_file_id, caption=caption, parse_mode="HTML")
        else:
            # في حالة عدم وجود صورة شخصية، يتم إرسال المعلومات فقط
            caption = await fetch_info_async(a)
            bot.send_message(a.chat.id, caption, parse_mode="HTML")
    
    except Exception as e:
        logging.error("Error in send_user_info_with_photo function: %s", e)
        bot.send_message(a.chat.id, "حدث خطأ أثناء جلب صورة المستخدم.", parse_mode="HTML")

# دالة لإرسال صورة المستخدم مع المعلومات
def send_user_info_with_photo(a: Message):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_user_info_with_photo_async(a))