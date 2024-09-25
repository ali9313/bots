# هذا الكود في الملف الثاني
from config import bot
from rtb import *  # استدعاء دالة قراءة الرتب من الملف الأول

# قاموس لتخزين عدد الرسائل لكل مستخدم
user_message_count = {}

def increment_user_message_count(user_id):
    """زيادة عداد الرسائل لكل مستخدم"""
    if user_id in user_message_count:
        user_message_count[user_id] += 1
    else:
        user_message_count[user_id] = 1

def get_user_message_count(user_id):
    """إرجاع عدد رسائل المستخدم"""
    return user_message_count.get(user_id, 0)

def get_user_role(user_id):
    """إرجاع رتبة المستخدم بناءً على معرفه"""
    members = load_roles()  # استدعاء دالة قراءة الرتب من الملف الأول
    return members.get(str(user_id), 'مواطن')  # إذا لم يكن له رتبة، افتراضي "مواطن"

def send_user_info(a):
    """إرسال معلومات المستخدم"""
    # إذا كان المستخدم يرد على شخص آخر
    if a.reply_to_message:
        user = a.reply_to_message.from_user  # الحصول على معلومات الشخص المُرد عليه
    else:
        user = a.from_user  # الحصول على معلومات الشخص الذي أرسل الأمر

    user_id = user.id  # الحصول على آيدي المستخدم
    user_name = user.first_name
    user_username = user.username if user.username else "معنده"
    user_messages = get_user_message_count(user_id)  # الحصول على عدد رسائل المستخدم
    user_role = get_user_role(user_id)  # استدعاء دالة لجلب رتبة المستخدم

    # إنشاء الكليشة مع الرتبة
    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ ID ⇢ {user_id}
    ‣ USER ⇢ @{user_username}
    ‣ ROLE ⇢ {user_role}  # عرض الرتبة
    ‣ MESSAGES ⇢ {user_messages}
    ⋆─┄─┄─┄─┄─⋆
    """

    # جلب الصورة الشخصية للمستخدم إذا كانت متاحة
    photos = bot.get_user_profile_photos(user.id)

    if photos.total_count > 0:
        bot.send_photo(a.chat.id, photos.photos[0][-1].file_id, caption=message_text)
    else:
        bot.send_message(a.chat.id, message_text)

@bot.message_handler(func=lambda a: True)
def handle_message(a):
    """معالجة الرسائل الجديدة"""
    user_id = a.from_user.id
    increment_user_message_count(user_id)  # زيادة عداد الرسائل
    send_user_info(a)  # استدعاء دالة معلومات المستخدم