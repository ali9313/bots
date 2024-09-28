from config import *  # إذا كانت تحتوي على إعدادات البوت مثل التوكن
from rep import *  # إذا كانت تحتوي على الدالة reply_func

# معالج الرسائل العامة
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        reply_func(a)  
    except Exception as e:
        print(f"حدث خطأ: {e}")

bot.polling(none_stop=True)