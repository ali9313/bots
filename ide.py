from config import *
from telebot.types import Message

# دالة لجلب معلومات المستخدم
def get_user_info(a: Message):
    user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
    full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
    user_id = user.id
    username = f"@{user.username}" if user.username else "لا يـوجـد"
    is_premium = "بـريميـوم" if user.is_premium else "عادي"
    
    info_message = f"• معلومـات إنشـاء حسـاب تيليجـرام 📑:\n"
    info_message += f"- الاسم: {full_name}\n"
    info_message += f"- الايــدي: {user_id}\n"
    info_message += f"- اليـوزر: {username}\n"
    info_message += f"- الحساب: {is_premium}\n"
    
    return info_message

# دالة لجلب الصور
def get_user_photos(a: Message):
    user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
    photos = bot.get_user_profile_photos(user.id)
    
    if photos.total_count > 0:
        photo_file_id = photos.photos[0][-1].file_id  # جلب أحدث صورة بأعلى دقة
        return photo_file_id
    else:
        return None

# أمر لعرض معلومات المستخدم
def send_user_info(a: Message):
    info_message = get_user_info(a)
    bot.reply_to(a, info_message)

# أمر لجلب صور المستخدم
def send_user_photo(a: Message):
    photo_file_id = get_user_photos(a)
    if photo_file_id:
        bot.send_photo(a.chat.id, photo_file_id)
    else:
        bot.reply_to(a, "لا يـوجـد صـور لهذا المستخدم.")