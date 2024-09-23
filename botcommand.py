from config import * 
# دالة التحقق من إذا كان المستخدم مشرفًا
def is_user_admin(bot, chat_id, user_id):
    user_status = bot.get_chat_member(chat_id, user_id).status
    return user_status in ['administrator', 'creator']

# دالة التعامل مع أمر الحظر
def my_cmd(a: Update, context: CallbackContext):
    message = a.message
    user = message.from_user
    chat_id = message.chat_id

    if message.text == "/ban" and message.reply_to_message:
        if is_user_admin(context.bot, chat_id, user.id):
            try:
                banned_user_id = message.reply_to_message.from_user.id
                banned_user_status = context.bot.get_chat_member(chat_id, banned_user_id).status
                
                # التحقق من أن المستخدم ليس مشرفًا أو منشئ المجموعة
                if banned_user_status not in ['administrator', 'creator']:
                    context.bot.ban_chat_member(chat_id, banned_user_id)
                    context.bot.send_message(chat_id, f"تم دفر: @{message.reply_to_message.from_user.username}")
                else:
                    context.bot.send_message(chat_id, "لا يمكن حظر مشرف أو منشئ المجموعة.")
            except Exception as e:
                context.bot.send_message(chat_id, f"حدث خطأ أثناء محاولة الحظر: {str(e)}")
        else:
            context.bot.send_message(chat_id, "عذراً، يجب أن تكون مشرفًا لاستخدام هذا الأمر.")