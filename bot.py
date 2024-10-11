import logging
import traceback
from config import *  
from rep import * 
from tfael import *
from ali_json import *
from tger import *

# إعداد تسجيل الأخطاء في ملف
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# معالج للأوامر
@bot.message_handler(commands=['check_dev', 'check_owner', 'check_basic_creator', 'check_admin', 'check_owner_id'])
def handle_commands(a):
    try:
        command = a.text.split()[0]
        logging.info(f"Received command: {command} from user {a.from_user.id} in chat {a.chat.id}")  # تسجيل الأوامر المستقبلة
        print(f"Processing command: {command}")  # طباعة لمتابعة التنفيذ في الكونسول
        
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
        logging.error(f"Error in handle_commands: {e}, user_id: {a.from_user.id}, chat_id: {a.chat.id}")
        traceback.print_exc()

# معالج للرسائل العامة
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        logging.info(f"Received message: {a.text} from user {a.from_user.id} in chat {a.chat.id}")  # تسجيل الرسائل المستقبلة
        print(f"Received message: {a.text}")  # طباعة الرسائل المستقبلة في الكونسول
        
        count_messages(a)  # عد الرسائل عند تلقي أي رسالة
        reply_func(a)  # الرد على الرسالة
        
    except Exception as e:
        logging.error(f"Error in echo_message: {e}, user_id: {a.from_user.id}, chat_id: {a.chat.id}")
        traceback.print_exc()

# بدء البوت
bot.polling(none_stop=True, timeout=60)