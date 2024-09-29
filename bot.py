from config import *  
from rep import * 
from ali_json import *
import traceback  # لاستيراد مكتبة تتبع الأخطاء

@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        reply_func(a)  
    except Exception as e:
        print(f"حدث خطأ: {e}")
        traceback.print_exc()  # لطباعة التفاصيل الكاملة للخطأ

bot.polling(none_stop=True, timeout=60)