from config import bot

def my_cmd(a):
    chat_member = bot.get_chat_member(a.chat.id, a.from_user.id)

    if chat_member.status in ['administrator', 'creator']:
        if a.reply_to_message:
            user_to_ban = a.reply_to_message.from_user.id
            chat_id = a.chat.id

            user_to_ban_member = bot.get_chat_member(chat_id, user_to_ban)
            if user_to_ban_member.status not in ['administrator', 'creator']:
                try:
                    bot.ban_chat_member(chat_id, user_to_ban)
                    bot.reply_to(a, f"تم دفر: @{a.reply_to_message.from_user.username if a.reply_to_message.from_user.username else 'Unknown'}")
                except Exception as e:
                    bot.reply_to(a, f"حدث خطأ: {str(e)}")
            elif user_to_ban_member.status in ['administrator', 'creator']:
                bot.reply_to(a, "مشرف هذا حبي")
            else:
                bot.reply_to(a, "يا مطي تريد تحظر نفسك !")
        else:
            bot.reply_to(a, "استخدم الامر بالرد ")
    else:
        bot.reply_to(a, "مسكين معندك صلاحيات")