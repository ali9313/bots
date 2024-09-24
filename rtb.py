from config import *
roles = {
    'عضو': 1,
    'مدير': 2,
    'مهيب': 3
}
MAHIIB_ID = 232499688 

# قائمة الأعضاء مع رتبهم
members = defaultdict(lambda: 'عضو')  # افتراضي: عضو

# دالة لمنح رتبة لأحد الأعضاء
def promote_user(a):
    user_id = a.from_user.id
    if user_id == MAHIIB_ID:  # فقط المهيب يمكنه منح الرتب
        if len(a.text.split()) > 1:
            target_user_id = int(a.text.split()[1])  # الحصول على ID المستخدم المستهدف
            new_role = a.text.split()[2] if len(a.text.split()) > 2 else 'عضو'  # الحصول على الرتبة الجديدة أو افتراضيًا 'عضو'
            
            if new_role in roles:
                members[target_user_id] = new_role
                bot.reply_to(a, f"تمت ترقية المستخدم {target_user_id} إلى رتبة {new_role}.")
            else:
                bot.reply_to(a, "رتبة غير صحيحة. يمكن أن تكون الرتبة: عضو، مدير، أو مهيب.")
        else:
            bot.reply_to(a, "يرجى تقديم ID المستخدم والرتبة التي تريد ترقيته لها.")
    else:
        bot.reply_to(a, "فقط المهيب يمكنه منح الرتب.")

# دالة لقراءة رتبة مستخدم
def read_role(a):
    user_id = a.from_user.id
    if a.reply_to_message:
        target_user_id = a.reply_to_message.from_user.id
        role = members[target_user_id]
        bot.reply_to(a, f"رتبة المستخدم {target_user_id} هي: {role}.")
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم الذي تريد معرفة رتبته.")