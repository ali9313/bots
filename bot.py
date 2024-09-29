from config import *  
from rep import * 
from tfael import *
from ali_json import *
import traceback  

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        reply_func(message)  
    except Exception as e:
        print(f"حدث خطأ: {e}")
        traceback.print_exc()  

@bot.message_handler(commands=['check_dev', 'check_owner', 'check_basic_creator', 'check_admin', 'check_owner_id'])
def handle_commands(message):
    try:
        command = message.text.split()[0]  
        if command == '/check_owner_id':
            check_owner_id(message)
        elif command == '/check_admin':
            check_admin(message)
        elif command == '/check_basic_creator':
            check_basic_creator(message)
        elif command == '/check_owner':
            check_owner(message)
        elif command == '/check_dev':
            check_dev(message)
    except Exception as e:
        print(f"حدث خطأ أثناء معالجة الأمر: {e}")
        traceback.print_exc()

# بدء البوت
bot.polling(none_stop=True, timeout=60)