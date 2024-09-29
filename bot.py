from config import *  
from rep import * 
from tfael import *
from ali_json import *
import traceback  

# معالج للأوامر
@bot.message_handler(commands=['check_dev', 'check_owner', 'check_basic_creator', 'check_admin', 'check_owner_id'])
def handle_commands(a):
    try:
        command = a.text.split()[0]  
        if command == '/check_owner_id':
            check_owner_id(a)
        elif command == '/check_admin':
            check_admin(a)
        elif command == '/check_basic_creator':
            check_basic_creator(a)
        elif command == '/check_owner':
            check_owner(a)
        elif command == '/check_dev':
            check_dev(a)
    except Exception as e:
        print(f"حدث خطأ أثناء معالجة الأمر: {e}")
        traceback.print_exc()

# معالج للرسائل العامة
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        reply_func(a)  
    except Exception as e:
        print(f"حدث خطأ: {e}")
        traceback.print_exc()  

# بدء البوت
bot.polling(none_stop=True, timeout=60)