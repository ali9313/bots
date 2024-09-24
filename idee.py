from config import bot
from collections import defaultdict
import os

# التأكد من استيراد members من الكود الثاني
from rtb import members  # استبدل your_roles_file باسم ملف الكود الثاني

# اسم الملف الذي سيتم تخزين عدد الرسائل فيه
messages_count_file = "backend/user_messages_count.txt"

# قاموس لتتبع عدد الرسائل لكل مستخدم
user_messages_count = defaultdict(int)

def load_user_messages_count():
    """تحميل عدد الرسائل من الملف"""
    if os.path.exists(messages_count_file):
        with open(messages_count_file, "r", encoding="utf-8") as f:
            for line in f:
                user_id, count = line.strip().split(":")
                user_messages_count[int(user_id)] = int(count)

def save_user_messages_count():
    """حفظ عدد الرسائل إلى الملف"""
    with open(messages_count_file, "w", encoding="utf-8") as f:
        for user_id, count in user_messages_count.items():
            f.write(f"{user_id}:{count}\n")

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

# تحميل عدد الرسائل عند بدء تشغيل البوت
load_user_messages_count()

@bot.message_handler(func=lambda a: True)
def handle_message(a):
    """معالجة الرسائل الجديدة"""
    user_messages_count[a.from_user.id] += 1  # زيادة عدد الرسائل للمستخدم
    save_user_messages_count()  # حفظ العدد بعد الزيادة