from config import *
from telebot.types import ChatPermissions

def mute_user(a):
    try:
        # التأكد من أن المستخدم يرد على رسالة عضو آخر
        if a.reply_to_message:
            user_id = a.reply_to_message.from_user.id
            chat_id = a.chat.id
            
            # إعداد الصلاحيات بحيث يتم منع المستخدم من إرسال الرسائل أو الوسائط
            permissions = ChatPermissions(can_send_messages=False)
            
            # كتم العضو لمدة معينة (بالثواني) أو إلى أجل غير مسمى إذا لم يتم تحديد وقت
            bot.restrict_chat_member(chat_id, user_id, permissions=permissions)
            
            (a, f"نلصم {a.reply_to_message.from_user.first_name}")
    except Exception as e:
        bot.reply_to(a, f"حدث خطأ: {str(e)}")