from config import *
from collections import defaultdict
import os

roles = {
    'مواطن': 1,           # تم تغيير اسم الرتبة إلى مواطن
    'موظف حكومي': 2,     # تم تغيير اسم الرتبة إلى موظف حكومي
    'رئيس الجمهورية': 3  # تم تغيير اسم الرتبة إلى رئيس الجمهورية
}
MAHIIB_ID = 232499688

# اسم الملف الذي سيتم تخزين الرتب فيه
roles_file = "backend/user_roles.txt"

# قائمة الأعضاء مع رتبهم
members = defaultdict(lambda: 'مواطن')  # افتراضي: مواطن

# دالة لتحميل الرتب من الملف
def load_roles():
    if os.path.exists(roles_file):
        with open(roles_file, "r", encoding="utf-8") as f:
            for line in f:
                user_id, role = line.strip().split(":")
                members[int(user_id)] = role

# دالة لحفظ الرتب إلى الملف
def save_roles():
    with open(roles_file, "w", encoding="utf-8") as f:
        for user_id, role in members.items():
            f.write(f"{user_id}:{role}\n")

# دالة لمنح رتبة لأحد الأعضاء من خلال الرد على رسالته
def promote_user(a):
    user_id = a.from_user.id
    if user_id == MAHIIB_ID:  # فقط رئيس الجمهورية يمكنه منح الرتب
        if a.reply_to_message:
            target_user_id = a.reply_to_message.from_user.id
            target_user_name = a.reply_to_message.from_user.first_name
            
            # الحصول على جميع الكلمات من الرسالة، ثم الانضمام إلى الكلمات التي تمثل الرتبة
            text_parts = a.text.split()
            new_role = ' '.join(text_parts[1:]) if len(text_parts) > 1 else 'مواطن'
            
            if new_role in roles:
                members[target_user_id] = new_role
                save_roles()  # حفظ الرتبة الجديدة
                bot.reply_to(a, f"تمت ترقية {target_user_name} إلى رتبة {new_role}.")
            else:
                bot.reply_to(a, "رتبة غير صحيحة. يمكن أن تكون الرتبة: مواطن، موظف حكومي، أو رئيس الجمهورية.")
        else:
            bot.reply_to(a, "يرجى الرد على رسالة المستخدم الذي تريد ترقيته.")
    else:
        bot.reply_to(a, "فقط رئيس الجمهورية يمكنه منح الرتب.")

# دالة لقراءة رتبة مستخدم من خلال الرد على رسالته
def read_role(a):
    if a.reply_to_message:
        target_user_id = a.reply_to_message.from_user.id
        target_user_name = a.reply_to_message.from_user.first_name
        role = members[target_user_id]
        
        if role == 'مواطن':
            bot.reply_to(a, f"هذا مواطن، له كل الاحترام.")
        elif role == 'موظف حكومي':
            bot.reply_to(a, f"هذا موظف حكومي، يقدم الخدمة العامة.")
        elif role == 'رئيس الجمهورية':
            bot.reply_to(a, f"هذا رئيس الجمهورية، له مكانة خاصة.")
        else:
            bot.reply_to(a, f"رتبة غير معروفة: {role}.")
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم الذي تريد معرفة رتبته.")

# دالة للتعامل مع الرسائل التي تُوجه للبوت
def handle_bot_reply(a):
    if a.reply_to_message and a.reply_to_message.from_user.id == bot.get_me().id:
        bot.reply_to(a, "اني بوت شتريد تعرف يعني 🙁")
        return True
    return False

# تعديل دالة الترويج ليتضمن رد البوت
def promote_user_with_reply(a):
    if handle_bot_reply(a):
        return
    promote_user(a)

# تعديل دالة قراءة الرتبة لتتضمن رد البوت
def read_role_with_reply(a):
    if handle_bot_reply(a):
        return
    read_role(a)

# تحميل الرتب عند بدء تشغيل البوت
load_roles()