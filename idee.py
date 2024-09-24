from config import bot
from collections import defaultdict

# التأكد من استيراد members من الكود الثاني
from rtb import members  # استبدل your_roles_file باسم ملف الكود الثاني

# قاموس لتتبع عدد الرسائل لكل مستخدم
user_messages_count = defaultdict(int)

def count_user_messages(message):
    # زيادة عدد الرسائل لكل مستخدم في المحادثة
    user_messages_count[message.from_user.id] += 1

def send_user_info(a):
    # إذا كان المستخدم يرد على شخص آخر
    if a.reply_to_message:
        user = a.reply_to_message.from_user  # الحصول على معلومات الشخص المُرد عليه
    else:
        user = a.from_user  # الحصول على معلومات الشخص الذي أرسل الأمر

    user_id = user.id  # الحصول على آيدي المستخدم
    user_name = user.first_name
    user_username = user.username if user.username else "معنده"
    user_role = members[user_id]  # التحقق من رتبة المستخدم من القائمة
    user_message_count = user_messages_count[user_id]  # الحصول على عدد الرسائل للمستخدم

    # إنشاء الكليشة مع الرتبة وعدد الرسائل
    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ ID ⇢ {user_id}
    ‣ USER ⇢ @{user_username}
    ‣ RANK ⇢ {user_role}
    ‣ MESSAGE ⇢ {user_message_count}
    ⋆─┄─┄─┄─┄─⋆
    """

    # جلب الصورة الشخصية للمستخدم إذا كانت متاحة
    photos = bot.get_user_profile_photos(user.id)

    if photos.total_count > 0:
        bot.send_photo(a.chat.id, photos.photos[0][-1].file_id, caption=message_text)
    else:
        bot.send_message(a.chat.id, message_text)

# يجب أن تقوم باستدعاء دالة count_user_messages عند تلقي رسالة جديدة
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    count_user_messages(message)