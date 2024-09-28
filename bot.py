from config import *  
from rep import * 
from ali_json import *
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        reply_func(a)  
    except Exception as e:
        print(f"حدث خطأ: {e}")

bot.polling(none_stop=True)