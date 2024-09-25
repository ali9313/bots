from config import *
from collections import defaultdict
import os

roles = {
    'مواطن': 1,           # تم تغيير اسم الرتبة إلى مواطن
    'موظف حكومي': 2,     # تم تغيير اسم الرتبة إلى موظف حكومي
    'رئيس الجمهورية': 3  # تم تغيير اسم الرتبة إلى رئيس الجمهورية
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
            for line in file:
                member_id, role_name = line.strip().split(',')
                members[member_id] = role_name

    # تعيين رتبة رئيس الجمهورية عند بداية تشغيل البوت
    if MAHIIB_ID not in members:
        members[MAHIIB_ID] = 'رئيس الجمهورية'

# دالة لحفظ الرتب إلى الملف
def save_roles():
    with open(roles_file, 'w', encoding='utf-8') as file:
        for member_id, role_name in members.items():
            file.write(f"{member_id},{role_name}\n")

# دالة لمنح رتبة لأحد الأعضاء من خلال الرد على رسالته
def promote_user(member_id, role_name):
    if role_name in roles:
        members[member_id] = role_name
        save_roles()  # حفظ التغييرات
        return f"تم منح الرتبة '{role_name}' للعضو {member_id}."
    else:
        return f"خطأ: الرتبة '{role_name}' غير موجودة."

# دالة لقراءة رتبة مستخدم من خلال الرسالة
def read_role(a):
    member_id = a.reply_to_message.from_user.id if a.reply_to_message else a.from_user.id  # الحصول على معرّف المستخدم
    role = members.get(member_id, 'مواطن')

    if role == 'مواطن':
        return "هذا مواطن مسكين على باب الله"
    elif role == 'موظف حكومي':
        return "هذا موظف ماشي حاله"
    elif role == 'رئيس الجمهورية':
        return "هذا رئيس الجمهورية تاج راسي وراسك"
    else:
        return "هذه رتبة غير معروفة"

# تحميل الرتب عند بدء تشغيل البوت
load_roles()