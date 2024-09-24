from config import *
from collections import defaultdict

roles = {
    'عضو': 1,
    'مدير': 2,
    'مهيب': 3
}
MAHIIB_ID = 232499688

# قائمة الأعضاء مع رتبهم
members = defaultdict(lambda: 'عضو')  # افتراضي: عضو

# دالة لمنح رتبة لأحد الأعضاء من خلال الرد على رسالته
def promote_user(a):
    user_id = a.from_user.id
    if user_id == MAHIIB_ID:  # فقط المهيب يمكنه منح الرتب
        if a.reply_to_message:
            target_user_id = a.reply_to_message.from_user.id  # الحصول على ID المستخدم المستهدف من الرسالة المُرد عليها
            target_user_name = a.reply_to_message.from_user.first_name  # الحصول على اسم الشخص المستهدف
            new_role = a.text.split()[1] if len(a.text.split()) > 1 else 'عضو'  # الحصول على الرتبة الجديدة أو افتراضيًا 'عضو'
            
            if new_role in roles:
                members[target_user_id] = new_role
                bot.reply_to(a, f"تمت ترقية {target_user_name} إلى رتبة {new_role}.")
            else:
                bot.reply_to(a, "رتبة غير صحيحة. يمكن أن تكون الرتبة: عضو، مدير، أو مهيب.")
        else:
            bot.reply_to(a, "يرجى الرد على رسالة المستخدم الذي تريد ترقيته.")
    else:
        bot.reply_to(a, "فقط المهيب يمكنه منح الرتب.")

# دالة لقراءة رتبة مستخدم من خلال الرد على رسالته
def read_role(a):
    if a.reply_to_message:
        target_user_id = a.reply_to_message.from_user.id
        target_user_name = a.reply_to_message.from_user.first_name  # الحصول على اسم الشخص المستهدف
        role = members[target_user_id]
        
        if role == 'عضو':
            bot.reply_to(a, f"هذا مجرد عضو الله مطيح حظه.")
        elif role == 'مدير':
            bot.reply_to(a, f"هذا المدير حمبي.")
        elif role == 'مهيب':
            bot.reply_to(a, f"هذا المهيب، له كل الاحترام.")
        else:
            bot.reply_to(a, f"رتبة غير معروفة: {role}.")
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم الذي تريد معرفة رتبته.")