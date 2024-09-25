from config import *
from rep import *
@bot.message_handler(content_types=['new_chat_members', 'left_chat_members'])
def cmbr(a):
    pass  # تم تعليق هذه الدالة

@bot.message_handler(commands=['start', 'ban'])
def my(a):
    pass  # تم تعليق هذه الدالة

def send_welcome(a):
    pass  # تم تعليق هذه الدالة

# معالج حذف الرسائل للمستخدمين المكتمين
@bot.message_handler(func=lambda a: a.from_user.id in muted_users)
def delete_muted_message(a):
    pass  # تم تعليق هذه الدالة

# معالج الرسائل العامة (يجب أن يأتي بعد معالج حذف الرسائل)
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        reply_func(a)
    except Exception as e:
        print(f"Error in 'echo_message' function: {str(e)}")
        bot.reply_to(a, f"حدث خطأ في معالجة الرسالة: {str(e)}")

# بدء تشغيل البوت
bot.polling()