from config import *
from telegram import Update
from telegram.ext import CallbackContext

# دالة التحقق من إذا كان المستخدم مشرفًا
def is_user_admin(a, chat_id, user_id):
    try:
        user_status = a.get_chat_member(chat_id, user_id).status
        return user_status in ['administrator', 'creator']
    except Exception:
        return False  # إذا كان هناك خطأ، اعتبر المستخدم غير مشرف

# دالة التعامل مع أمر الحظر
def my_cmd(update: Update, context: CallbackContext):
    message = update.message
    user = message.from_user
    chat_id = message.chat.id  # استخدام chat.id بدلاً من chat_id

    if message.text == "/ban" and message.reply_to_message:
        if is_user_admin(context.bot, chat_id, user.id):
            try:
                banned_user_id = message.reply_to_message.from_user.id
                banned_user_status = context.bot.get_chat_member(chat_id, banned_user_id).status
                
                # التحقق من أن المستخدم ليس مشرفًا أو منشئ المجموعة
                if banned_user_status not in ['administrator', 'creator']:
                    context.bot.ban_chat_member(chat_id, banned_user_id)
                    username = message.reply_to_message.from_user.username or "المستخدم"
                    context.bot.send_message(chat_id, f"تم حظر: @{username}")
                else:
                    context.bot.send_message(chat_id, "لا يمكن حظر مشرف أو منشئ المجموعة.")
            except Exception as e:
                context.bot.send_message(chat_id, f"حدث خطأ أثناء محاولة الحظر: {str(e)}")
        else:
            context.bot.send_message(chat_id, "عذراً، يجب أن تكون مشرفًا لاستخدام هذا الأمر.")