from config import *
from collections import defaultdict
import os

roles = {
    'مواطن': 1,
    'موظف حكومي': 2,
    'رئيس الجمهورية': 3
}
MAHIIB_ID = 232499688  # معرف رئيس الجمهورية

# اسم الملف الذي سيتم تخزين الرتب فيه
roles_file = "backend/user_roles.txt"

# قائمة الأعضاء مع رتبهم
members = defaultdict(lambda: 'مواطن')  # افتراضي: مواطن

# دالة لتحميل الرتب من الملف
def load_roles():
    if os.path.exists(roles_file):
        with open(roles_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:  # تحقق مما إذا كان الملف غير فارغ
                for line in lines:
                    line = line.strip()
                    if not line:  # تجاهل السطر الفارغ
                        continue
                    try:
                        member_id, role_name = line.split(',', 1)
                        members[member_id] = role_name
                    except ValueError:
                        print(f"خطأ في قراءة السطر: {line}")  # تسجيل الخطأ في قراءة السطر

    # تعيين رتبة رئيس الجمهورية عند بداية تشغيل البوت
    if MAHIIB_ID not in members:
        members[MAHIIB_ID] = 'رئيس الجمهورية'

# دالة لحفظ الرتب إلى الملف
def save_roles():
    with open(roles_file, 'w', encoding='utf-8') as file:
        for member_id, role_name in members.items():
            file.write(f"{member_id},{role_name}\n")

# دالة لمنح رتبة لأحد الأعضاء من خلال الرسالة
def promote_user(a):
    member_id = a.reply_to_message.from_user.id if a.reply_to_message else a.from_user.id  # الحصول على معرّف المستخدم

    # استخراج الرتبة من نص الرسالة (إزالة الكلمة الأولى "رفع")
    role_name = ' '.join(a.text.split()[1:])  # أخذ كل الكلمات بعد الكلمة الأولى

    if role_name == 'رئيس الجمهورية':
        bot.reply_to(a, "رئيس الجمهورية واحد ميصير ثنين")
    elif role_name in roles:
        # تغيير الرتبة المعروفة فقط
        current_role = members[member_id]
        members[member_id] = role_name
        save_roles()  # حفظ التغييرات

        # تحديد الرد المناسب بناءً على الرتبة الجديدة
        if role_name == 'مواطن':
            bot.reply_to(a, f"هذا اصلا مواطن {a.reply_to_message.from_user.first_name}.")
        elif role_name == 'موظف حكومي':
            bot.reply_to(a, f"حلو صار موظف {a.reply_to_message.from_user.first_name}.")
        else:
            bot.reply_to(a, f"تم منح الرتبة '{role_name}' للعضو {a.reply_to_message.from_user.first_name}.")
    else:
        # السماح بإضافة رتبة جديدة
        current_role = members[member_id]
        members[member_id] = role_name
        save_roles()  # حفظ التغييرات
        bot.reply_to(a, f"تم منح الرتبة الجديدة '{role_name}' للعضو {a.reply_to_message.from_user.first_name}.")

# دالة لقراءة رتبة مستخدم من خلال الرسالة
def read_role(a):
    member_id = a.reply_to_message.from_user.id if a.reply_to_message else a.from_user.id  # الحصول على معرّف المستخدم
    role = members.get(member_id, 'مواطن')

    # التحقق من الرتبة الأعلى
    current_role_value = roles.get(role, 0)
    higher_roles = {name: value for name, value in roles.items() if value > current_role_value}
    
    # إذا كان هناك رتبة أعلى، اختر الأعلى
    if higher_roles:
        highest_role = max(higher_roles, key=roles.get)
        role = highest_role
    
    # تحديد الرد المناسب بناءً على الرتبة
    if role == 'مواطن':
        response = "هذا مواطن مسكين على باب الله"
    elif role == 'موظف حكومي':
        response = "هذا موظف ماشي حاله"
    elif role == 'رئيس الجمهورية':
        response = "هذا رئيس الجمهورية تاج راسي وراسك"
    else:
        response = "هذه رتبة غير معروفة"
    
    # إرجاع الرد إلى المستخدم
    bot.reply_to(a, response)

# تحميل الرتب عند بدء تشغيل البوت
load_roles()