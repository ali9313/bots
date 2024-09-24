from config import *
from telebot.types import ChatPermissions

# قائمة للمستخدمين الذين سيتم حذف رسائلهم بشكل تلقائي
muted_users = set()

def mute_user(a):
    try:
        # التأكد من أن المستخدم يرد على رسالة عضو آخر
        if a.reply_to_message:
            user_id = a.reply_to_message.from_user.id
            chat_id = a.chat.id
            
            # إضافة المستخدم إلى قائمة الممنوعين من إرسال الرسائل
            muted_users.add(user_id)
            
            # إبلاغ الشخص الذي أرسل الأمر بنجاح العملية
            bot.reply_to(a, f"نلصم {a.reply_to_message.from_user.first_name}")
    except Exception as e:
        bot.reply_to(a, f"حدث خطأ: {str(e)}")