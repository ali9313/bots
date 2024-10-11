import random
import logging
from config import *
from telebot.types import Message
from ali_json import programmer_ali, owner, creator, owner_id_ali, is_basic_creator, dev, basic_dev

# إعداد logging لتسجيل الأخطاء في ملف log.txt
logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# قاموس لتخزين عدد الرسائل لكل مستخدم في كل دردشة
message_counts = {}

# قاموس للنصوص والزخارف
styles = {
    "greetings": [
        "المختصر انتِ شي حلو محد يشبهه💕 🫶",
        "يا جمالك! 😍",
        "أنت نجم ساطع في السماء! 🌟",
        "يا مشع 🕶️✨"
    ],
    "decorations": [
        "✦ ", "➼ ", "➤ ", "⤎ ", "𓅫 "
    ]
}

# دالة لاختيار نص وزخرفة عشوائية
def get_random_style():
    ali_text = random.choice(styles['greetings'])
    adot = random.choice(styles['decorations'])
    return ali_text, adot

# دالة لحساب عدد الرسائل الخاصة بالمستخدم
def get_message_count(user_id, chat_id):
    if chat_id in message_counts:
        return message_counts[chat_id].get(user_id, 0)
    return 0

# دالة للتحقق من رتبة المستخدم
def check_user_rank(user_id, chat_id):
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

# دالة لجلب معلومات المستخدم
def fetch_info(a: Message):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        full_name = user.first_name + ' ' + (user.last_name if user.last_name else "")
        user_id = user.id
        username = f"@{user.username}" if user.username else "لا يـوجـد"
        
        # جلب معلومات البايو باستخدام get_chat
        user_chat = bot.get_chat(user_id)
        user_bio = user_chat.bio if user_chat.bio else "لا يـوجـد"
        
        # جلب عدد الرسائل الفعلي
        aaa = get_message_count(user_id, a.chat.id)
        
        # تحديد مستوى التفاعل بناءً على عدد الرسائل
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
            al = "غنبله  💣"
        else:
            al = "نار وشرر  🏆"

        # الحصول على رتبة المستخدم
        user_rank = check_user_rank(user_id, a.chat.id)

        # اختيار نص وزخرفة عشوائية
        ali_text, adot = get_random_style()
        
        caption = f"<b>{ali_text} </b>\n"
        caption += f"<b>{adot}الاســم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>"
        caption += f"\n<b>{adot}اليـوزر    ⤎  {username}</b>"
        caption += f"\n<b>{adot}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{adot}الرتبــه    ⤎ {user_rank} 𓅫 </b>\n"  # إضافة رتبة المستخدم
        caption += f"<b>{adot}الرسائل  ⤎</b>  {aaa} 💌\n"
        caption += f"<b>{adot}التفاعل  ⤎</b>  {al}\n"  # إضافة مستوى التفاعل
        caption += f"<b>{adot}البايـو     ⤎  {user_bio}</b>\n"
        
        return caption
    except Exception as e:
        logging.error("Error in fetch_info function: %s", e)
        return "حدث خطأ أثناء جلب معلومات المستخدم."

# دالة لإرسال صورة الملف الشخصي مع الكابشن
def send_user_info_with_photo(a: Message):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        user_id = user.id
        
        # جلب صورة الملف الشخصي للمستخدم
        photos = bot.get_user_profile_photos(user_id)
        
        # التحقق من وجود صور للمستخدم
        if photos.total_count > 0:
            # جلب أول صورة من الصور المتاحة
            photo_file_id = photos.photos[0][-1].file_id
            
            # جلب الكابشن (المعلومات) 
            caption = fetch_info(a)
            
            # إرسال الصورة مع الكابشن
            bot.send_photo(a.chat.id, photo_file_id, caption=caption, parse_mode="HTML")
        else:
            # في حالة عدم وجود صورة شخصية، يتم إرسال المعلومات فقط
            caption = fetch_info(a)
            bot.send_message(a.chat.id, caption, parse_mode="HTML")
    
    except Exception as e:
        logging.error("Error in send_user_info_with_photo function: %s", e)
        bot.send_message(a.chat.id, "حدث خطأ أثناء جلب صورة المستخدم.", parse_mode="HTML")

# دالة لحساب عدد الرسائل
def count_messages(a: Message):
    chat_id = a.chat.id
    user_id = a.from_user.id
    if chat_id not in message_counts:
        message_counts[chat_id] = {}
    if user_id in message_counts[chat_id]:
        message_counts[chat_id][user_id] += 1
    else:
        message_counts[chat_id][user_id] = 1