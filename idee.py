from config import bot
import os

# التأكد من استيراد members من الكود الثاني
from rtb import members  # استبدل your_roles_file باسم ملف الكود الثاني

# اسم الملف الذي سيتم تخزين معلومات المستخدمين فيه
messages_count_file = "backend/user_messages_info.txt"

def load_user_messages_info():
    """تحميل معلومات المستخدمين من الملف (مثل الأسماء والرتب)"""
    if os.path.exists(messages_count_file):
        with open(messages_count_file, "r", encoding="utf-8") as f:
            for line in f:
                user_id, user_name, user_role = line.strip().split(":")
                # هنا يمكنك تخزين البيانات في مكان مناسب
                print(f"Loaded user info - ID: {user_id}, Name: {user_name}, Role: {user_role}")

def save_user_messages_info(user_id, user_name, user_role):
    """حفظ معلومات المستخدم إلى الملف"""
    with open(messages_count_file, "a", encoding="utf-8") as f:
        f.write(f"{user_id}:{user_name}:{user_role}\n")

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

    # إنشاء الكليشة مع الرتبة
    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ ID ⇢ {user_id}
    ‣ USER ⇢ @{user_username}
    ‣ RANK ⇢ {user_role}
    ⋆─┄─┄─┄─┄─⋆
    """

    # جلب الصورة الشخصية للمستخدم إذا كانت متاحة
    photos = bot.get_user_profile_photos(user.id)

    if photos.total_count > 0:
        bot.send_photo(a.chat.id, photos.photos[0][-1].file_id, caption=message_text)
    else:
        bot.send_message(a.chat.id, message_text)

# تحميل معلومات المستخدمين عند بدء تشغيل البوت
load_user_messages_info()

@bot.message_handler(func=lambda a: True)
def handle_message(a):
    """معالجة الرسائل الجديدة"""
    # يمكنك استدعاء send_user_info هنا إذا كانت هناك حاجة لذلك
    if a.text.startswith('/info'):  # على سبيل المثال، استخدام /info لاستعراض المعلومات
        send_user_info(a)