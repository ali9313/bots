from config import *  
from rep import * 
from tfael import *
import traceback  # لاستيراد مكتبة تتبع الأخطاء

@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        # تحقق مما إذا كانت الرسالة تحتوي على الأمر 'تفعيل'
        if a.text == "/تفعيل":
            update_owners(a)  # استدعاء دالة update_owners مباشرة
        else:
            reply_func(a)  # استدعاء الدالة reply_func لبقية الرسائل
    except Exception as e:
        print(f"حدث خطأ: {e}")
        traceback.print_exc()  # لطباعة التفاصيل الكاملة للخطأ

bot.polling(none_stop=True, timeout=60)