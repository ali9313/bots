from config import bot

def ban_user(a):
    chat_member = bot.get_chat_member(a.chat.id, message.from_user.id)

    if chat_member.status in ['administrator', 'creator']:
        if a.reply_to_message:
            user_to_ban = a.reply_to_message.from_user.id
            chat_id = a.chat.id


            user_to_ban_member = bot.get_chat_member(chat_id, user_to_ban)
            if user_to_ban_member.status not in ['administrator', 'creator']:
                try:
                    bot.ban_chat_member(chat_id, user_to_ban)
                    bot.send_message(chat_id, f"تم حظر المستخدم @{message.reply_to_message.from_user.username if message.reply_to_message.from_user.username else 'Unknown'}")
                except Exception as e:
                    bot.send_message(chat_id, f"حدث خطأ: {str(e)}")
            else:
                bot.send_message(chat_id, "لا يمكنك حظر مشرف!")
        else:
            bot.send_message(a.chat.id, "يرجى الرد على رسالة المستخدم الذي تريد حظره.")
    else:
        bot.send_message(a.chat.id, "ليس لديك الأذونات اللازمة لحظر المستخدمين.")
