from config import *
from rep import *

# معالج الرسائل العامة
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        reply_func(a)  # استدعاء الدالة فقط
    except Exception as e:
        print(f"Error in 'echo_message' function: {str(e)}")
        bot.reply_to(a, f"حدث خطأ في معالجة الرسالة: {str(e)}")

# بدء تشغيل البوت
bot.polling()