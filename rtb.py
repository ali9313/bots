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

# قائمة الأعضاء مع رتبهم (تحتوي على قائمة من الرتب)
members = defaultdict(lambda: ['مواطن'])  # افتراضي: قائمة تحتوي على "مواطن"

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
                        if role_name in roles:  # إضافة الرتبة فقط إذا كانت معرفة
                            members[member_id].append(role_name)
                    except ValueError:
                        print(f"خطأ في قراءة السطر: {line}")  # تسجيل الخطأ في قراءة السطر

    # تعيين رتبة رئيس الجمهورية عند بداية تشغيل البوت
    if MAHIIB_ID not in members:
        members[MAHIIB_ID] = ['رئيس الجمهورية']

# دالة لحفظ الرتب إلى الملف
def save_roles():
    with open(roles_file, 'w', encoding='utf-8') as file:
        for member_id, role_list in members.items():
            for role_name in role_list:
                file.write(f"{member_id},{role_name}\n")

# دالة لمنح رتبة لأحد الأعضاء من خلال الرسالة
def promote_user(a):
    member_id = a.reply_to_message.from_user.id if a.reply_to_message else a.from_user.id  # الحصول على معرّف المستخدم

    # استخراج الرتبة من نص الرسالة (إزالة الكلمة الأولى "رفع")
    role_name = ' '.join(a.text.split()[1:])  # أخذ كل الكلمات بعد الكلمة الأولى

    if role_name == 'رئيس الجمهورية':
        bot.reply_to(a, "رئيس الجمهورية واحد ميصير ثنين")
    elif role_name in roles:  # فقط الرتب المعرفة في القائمة
        if role_name not in members[member_id]:
            members[member_id].append(role_name)  # إضافة الرتبة إذا لم تكن موجودة مسبقًا
        save_roles()  # حفظ التغييرات

        # تحديد الرد المناسب بناءً على الرتبة الجديدة
        if role_name == 'مواطن':
            bot.reply_to(a, f"هذا اصلا مواطن {a.reply_to_message.from_user.first_name}.")
        elif role_name == 'موظف حكومي':
            bot.reply_to(a, f"حلو صار موظف {a.reply_to_message.from_user.first_name}.")
        else:
            bot.reply_to(a, f"تم منح الرتبة '{role_name}' للعضو {a.reply_to_message.from_user.first_name}.")
    else:
        # إذا كانت الرتبة غير معرفة
        bot.reply_to(a, f"خطأ: الرتبة '{role_name}' غير موجودة في القائمة.")

# دالة لقراءة رتبة مستخدم من خلال الرسالة
def read_role(a):
    # الحصول على معرف المستخدم الذي تم الرد على رسالته
    if not a.reply_to_message:
        bot.reply_to(a, "الرجاء الرد على رسالة العضو لقراءة رتبته.")
        return
    
    member_id = a.reply_to_message.from_user.id  # الحصول على معرف المستخدم
    user_roles = members.get(member_id, ['مواطن'])  # استرجاع قائمة الرتب

    # البحث عن الرتبة الأعلى بناءً على القيم المعرفة في قاموس `roles`
    highest_role = max(user_roles, key=lambda role: roles.get(role, 0))

    # تحديد الرد المناسب بناءً على الرتبة
    if highest_role == 'مواطن':
        response = "هذا مواطن مسكين على باب الله"
    elif highest_role == 'موظف حكومي':
        response = "هذا موظف ماشي حاله"
    elif highest_role == 'رئيس الجمهورية':
        response = "هذا رئيس الجمهورية تاج راسي وراسك"
    else:
        response = "هذه رتبة غير معروفة"
    
    # إرجاع الرد إلى المستخدم
    bot.reply_to(a, response)

# تحميل الرتب عند بدء تشغيل البوت
load_roles()