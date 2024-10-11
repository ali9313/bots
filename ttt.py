import random
import logging
from config import *
from telebot.types import Message
from ali_json import programmer_ali, owner, creator, owner_id_ali, is_basic_creator, dev, basic_dev

# إعداد تسجيل الأخطاء في ملف
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

message_counts = {}

styles = {
    "greetings": [
        "المختصر انت شي حلو محد يشبهه💕 🫶",
        "يا جمالك! 😍",
        "أنت نجم ساطع في السماء! 🌟",
        "يا مشع 🕶️✨"
    ],
    "decorations": [
        "✦ ", "➼ ", "➤ ", "⤎ "
    ]
}

def get_random_style():
    ali_text = random.choice(styles['greetings'])
    adot = random.choice(styles['decorations'])
    return ali_text, adot

def get_message_count(user_id, chat_id):
    if chat_id in message_counts:
        return message_counts[chat_id].get(user_id, 0)
    return 0

def check_user_rank(user_id, chat_id):
    try:
        if programmer_ali(user_id):
            return "مبرمج السورس"
        elif owner(user_id, chat_id):
            return "مالك"
        elif creator(user_id, chat_id):
            return "منشئ"
        elif owner_id_ali(user_id):
            return "مطور اساسي"
        elif is_basic_creator(user_id):
            return "منشئ أساسي"
        elif dev(user_id):
            return "مطور"
        elif basic_dev(user_id):
            return "مطور ثانوي"
        else:
            return "عضو"
    except Exception as e:
        logging.error(f"Error in check_user_rank function: {e}, user_id: {user_id}, chat_id: {chat_id}")
        return "حدث خطأ أثناء التحقق من رتبة المستخدم."

def fetch_info(a: Message):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        full_name = user.first_name + ' ' + (user.last_name if user.last_name else "")
        user_id = user.id
        username = f"@{user.username}" if user.username else "لا يـوجـد"
        
        user_chat = bot.get_chat(user_id)
        user_bio = user_chat.bio if user_chat.bio else "لا يـوجـد"
        
        aaa = get_message_count(user_id, a.chat.id)
        
        if aaa < 100: 
            al = "غير متفاعل  🗿"
        elif aaa < 500:
            al = "ضعيف  🗿"
        elif aaa < 700:
            al = "شد حيلك  🏇"
        elif aaa < 1000:
            al = "ماشي الحال  🏄🏻‍♂"
        elif aaa < 2000:
            al = "ملك التفاعل  🎖"
        elif aaa < 3000:
            al = "امبراطور التفاعل  🥇"
        elif aaa < 4000:
            al = "قنبله  💣"
        else:
            al = "نار وشرر  🏆"

        user_rank = check_user_rank(user_id, a.chat.id)

        ali_text, adot = get_random_style()
        
        caption = f"<b>{ali_text} </b>\n"
        caption += f"<b>{adot}الاســم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>"
        caption += f"\n<b>{adot}اليـوزر    ⤎  {username}</b>"
        caption += f"\n<b>{adot}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{adot}الرتبــه    ⤎ {user_rank} </b>\n"  
        caption += f"<b>{adot}الرسائل  ⤎</b>  {aaa} 💌\n"
        caption += f"<b>{adot}التفاعل  ⤎</b>  {al}\n"  
        caption += f"<b>{adot}البايـو     ⤎  {user_bio}</b>\n"
        
        return caption
    except Exception as e:
        logging.error(f"Error in fetch_info function: {e}, user_id: {a.from_user.id}, chat_id: {a.chat.id}")
        return "حدث خطأ أثناء جلب معلومات المستخدم."

def send_user_info_with_photo(a: Message):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        user_id = user.id
        
        photos = bot.get_user_profile_photos(user_id)
        
        if photos.total_count > 0:
            photo_file_id = photos.photos[0][-1].file_id
            
            caption = fetch_info(a)
            
            bot.send_photo(a.chat.id, photo_file_id, caption=caption, parse_mode="HTML")
        else:
            caption = fetch_info(a)
            bot.send_message(a.chat.id, caption, parse_mode="HTML")
    
    except Exception as e:
        logging.error(f"Error in send_user_info_with_photo function: {e}, user_id: {user_id}, chat_id: {a.chat.id}")
        bot.send_message(a.chat.id, "حدث خطأ أثناء جلب صورة المستخدم.", parse_mode="HTML")

def count_messages(a: Message):
    try:
        chat_id = a.chat.id
        user_id = a.from_user.id
        if chat_id not in message_counts:
            message_counts[chat_id] = {}
        if user_id in message_counts[chat_id]:
            message_counts[chat_id][user_id] += 1
        else:
            message_counts[chat_id][user_id] = 1
    except Exception as e:
        logging.error(f"Error in count_messages function: {e}, user_id: {user_id}, chat_id: {chat_id}")

def handle_add_message_command(a: Message):
    try:
        text = a.text
        
        if text.startswith("اضف رسائله"):
            parts = text.split()  
            if len(parts) == 3 and parts[2].isdigit():  
                count = int(parts[2])  
                user_id = a.reply_to_message.from_user.id if a.reply_to_message else a.from_user.id
                chat_id = a.chat.id
                
                if chat_id not in message_counts:
                    message_counts[chat_id] = {}
                if user_id in message_counts[chat_id]:
                    message_counts[chat_id][user_id] += count
                else:
                    message_counts[chat_id][user_id] = count
                
                bot.send_message(a.chat.id, f"تم إضافة {count} رسائل.")
            else:
                bot.send_message(a.chat.id, "يرجى إدخال الأمر بالشكل الصحيح، مثال: اضف رسائله 356")
        else:
            bot.send_message(a.chat.id, "الأمر غير صحيح.")
    
    except Exception as e:
        logging.error(f"Error in handle_add_message_command function: {e}, user_id: {a.from_user.id}, chat_id: {a.chat.id}")
        bot.send_message(a.chat.id, "حدث خطأ أثناء معالجة الأمر.", parse_mode="HTML")