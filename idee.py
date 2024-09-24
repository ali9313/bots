from config import bot

# التأكد من استيراد members من الكود الثاني
from rtb import members  # استبدل your_roles_file باسم ملف الكود الثاني

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
    user_role = members.get(user_id, "غير محدد")  # التحقق من رتبة المستخدم من القائمة
    user_messages = get_user_message_count(user_id)  # الحصول على عدد رسائل المستخدم

    # إنشاء الكليشة مع الرتبة وعدد الرسائل
    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ ID ⇢ {user_id}
    ‣ USER ⇢ @{user_username}
    ‣ RANK ⇢ {user_role}
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
    if a.text.startswith('/info'):  # على سبيل المثال، استخدام /info لاستعراض المعلومات
        send_user_info(a)