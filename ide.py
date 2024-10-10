import logging
from config import *
from telebot.types import Message

# إعداد logging لتسجيل الأخطاء في ملف log.txt
logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# قاموس لتخزين عدد الرسائل لكل مستخدم في كل دردشة
message_counts = {}

# دالة لحساب عدد الرسائل الخاصة بالمستخدم
def get_message_count(user_id, chat_id):
    # استخدام القاموس لتخزين عدد الرسائل
    if chat_id in message_counts:
        return message_counts[chat_id].get(user_id, 0)
    return 0

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
        zzz = get_message_count(user_id, a.chat.id)
        
        # تحديد مستوى التفاعل بناءً على عدد الرسائل
        if zzz < 100: 
            zelzzz = "غير متفاعل  🗿"
        elif zzz < 500:
            zelzzz = "ضعيف  🗿"
        elif zzz < 700:
            zelzzz = "شد حيلك  🏇"
        elif zzz < 1000:
            zelzzz = "ماشي الحال  🏄🏻‍♂"
        elif zzz < 2000:
            zelzzz = "ملك التفاعل  🎖"
        elif zzz < 3000:
            zelzzz = "امبراطور التفاعل  🥇"
        elif zzz < 4000:
            zelzzz = "غنبله  💣"
        else:
            zelzzz = "نار وشرر  🏆"

        ZED_TEXT = "المختصر انتِ شي حلو محد يشبهه💕 🫶"
        ZEDM = "✦ "
        
        caption = f"<b>{ZED_TEXT} </b>\n"
        caption += f"<b>{ZEDM}الاســم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>"
        caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
        caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{ZEDM}الرتبــه    ⤎ العضو 𓅫 </b>\n"
        caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz} 💌\n"
        caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n"  # إضافة مستوى التفاعل
        caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
        
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
            photo_file_id = photos.photos[0][-1].file_id  # جلب أعلى جودة للصورة
            
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