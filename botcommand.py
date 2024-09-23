from config import *
def is_user_admin(chat_id, user_id):
    try:
        user_status = bot.get_chat_member(chat_id, user_id).status
        return user_status in ['administrator', 'creator']
    except Exception:
        return False  
def my_cmd(a):
    user = a.from_user
    chat_id = a.chat.id 

    if a.reply_to_message:
        if is_user_admin(chat_id, user.id):
            try:
                banned_user_id = a.reply_to_message.from_user.id
                banned_user_status = bot.get_chat_member(chat_id, banned_user_id).status
                if banned_user_status not in ['administrator', 'creator']:
                    bot.ban_chat_member(chat_id, banned_user_id)
                    username = a.reply_to_message.from_user.username or "المستخدم"
                    bot.send_message(chat_id, f"تم دفر: @{username}")
                else:
                    bot.reply_to(chat_id, "ما اكدر احظر مشرف اعذرني ")
            except Exception as e:
                bot.send_message(chat_id, f"اكو شي غلط: {str(e)}")
        else:
            bot.send_message(chat_id, "انت مو مشرف يا مطي ")
    else:
        bot.send_message(chat_id, "استخدم الامر بالرد ")
