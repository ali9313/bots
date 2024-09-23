from config import *
def is_user_admin(chat_id, user_id):
    try:
        user_status = bot.get_chat_member(chat_id, user_id).status
        return user_status in ['administrator', 'creator']
    except Exception:
        return False  
def my_cmd(a):
    user = a.from_user
    chat_id = a.chat.id  # استخدام chat.id بدلاً من chat_id

    if a.reply_to_message:
        if is_user_admin(chat_id, user.id):
            try:
                banned_user_id = a.reply_to_message.from_user.id
                banned_user_status = bot.get_chat_member(chat_id, banned_user_id).status
                
                # التحقق من أن المستخدم ليس مشرفًا أو منشئ المجموعة
                if banned_user_status not in ['administrator', 'creator']:
                    bot.ban_chat_member(chat_id, banned_user_id)
                    username = a.reply_to_message.from_user.username or "المستخدم"
                    bot.send_message(chat_id, f"تم حظر: @{username}")
                else:
                    bot.send_message(chat_id, "لا يمكن حظر مشرف أو منشئ المجموعة.")
            except Exception as e:
                bot.send_message(chat_id, f"حدث خطأ أثناء محاولة الحظر: {str(e)}")
        else:
            bot.send_message(chat_id, "عذراً، يجب أن تكون مشرفًا لاستخدام هذا الأمر.")
    else:
        bot.send_message(chat_id, "يرجى الرد على رسالة المستخدم الذي تريد حظره.")
