from config import bot
from collections import defaultdict

# قاموس لتخزين عدد الرسائل لكل مستخدم
user_message_count = {}

# نقوم بتحميل الرتب من الملف الأول
roles_file = "backend/user_roles.txt"

# قائمة الأعضاء مع رتبهم (تحتوي على قائمة من الرتب)
members = defaultdict(lambda: ['مواطن'])  # افتراضي: قائمة تحتوي على "مواطن"

# تحميل الرتب من الملف الأول
def load_roles():
    if os.path.exists(roles_file):
        with open(roles_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        member_id, role_name = line.split(',', 1)
                        members[member_id].append(role_name)
                    except ValueError:
                        print(f"خطأ في قراءة السطر: {line}")

# استدعاء دالة تحميل الرتب عند بدء تشغيل البرنامج
load_roles()

def increment_user_message_count(user_id):
    """زيادة عداد الرسائل لكل مستخدم"""
    if user_id in user_message_count:
        user_message_count[user_id] += 1
    else:
        user_message_count[user_id] = 1

def get_user_message_count(user_id):
    """إرجاع عدد رسائل المستخدم"""
    return user_message_count.get(user_id, 0)

def get_highest_role(user_id):
    """إرجاع أعلى رتبة للمستخدم"""
    user_roles = members.get(str(user_id), ['مواطن'])  # الحصول على الرتب للمستخدم
    roles = {
        'مواطن': 1,
        'موظف حكومي': 2,
        'رئيس الجمهورية': 3
    }
    highest_role = max(user_roles, key=lambda role: roles.get(role, 0))  # اختيار أعلى رتبة
    return highest_role

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
    user_role = get_highest_role(user_id)  # الحصول على أعلى رتبة للمستخدم

    # إنشاء الكليشة مع الرتبة
    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ ID ⇢ {user_id}
    ‣ USER ⇢ @{user_username}
    ‣ RANK ⇢ {user_role}  # عرض الرتبة
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