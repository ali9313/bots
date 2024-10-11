import logging
import traceback
from config import *  
from rep import * 
from tfael import *
from ali_json import *
from tger import *
from ttt import *

# إعداد تسجيل الأخطاء في ملف
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# دالة تجزئة الرسالة والتحقق من "اضف رسائله" مع عدد
def check_command_and_execute(a):
    try:
        words = a.text.split()

        # التأكد من أن الرسالة تحتوي على 3 أجزاء: "اضف رسائله" + عدد
        if len(words) == 3 and words[0] == "اضف" and words[1] == "رسائله" and words[2].isdigit():
            count = int(words[2])  # تحويل الجزء الثالث (العدد) إلى عدد صحيح
            print(f"تم التعرف على الأمر 'اضف رسائله' مع العدد {count}")

            # استدعاء الدالة لإضافة عدد الرسائل للمستخدم
            handle_add_message_command(a)

        else:
            print("الرسالة لا تطابق النمط المطلوب.")
    except Exception as e:
        logging.error(f"Error in check_command_and_execute: {e}, user_id: {a.from_user.id}, chat_id: {a.chat.id}")
        traceback.print_exc()

# دالة استدعاء افتراضية لإضافة عدد الرسائل (يمكنك تخصيصها لاحقًا)
def handle_add_message_command(a):
    try:
        user_id = a.reply_to_message.from_user.id if a.reply_to_message else a.from_user.id
        chat_id = a.chat.id

        if chat_id not in message_counts:
            message_counts[chat_id] = {}
        if user_id in message_counts[chat_id]:
            message_counts[chat_id][user_id] += 1
        else:
            message_counts[chat_id][user_id] = 1

        bot.send_message(a.chat.id, f"تم إضافة رسائل.")
    except Exception as e:
        logging.error(f"Error in handle_add_message_command: {e}, user_id: {a.from_user.id}, chat_id: {a.chat.id}")
        traceback.print_exc()

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
        check_command_and_execute(a)  # التحقق من الأمر "اضف رسائله" وتنفيذ الدالة

    except Exception as e:
        logging.error(f"Error in echo_message: {e}, user_id: {a.from_user.id}, chat_id: {a.chat.id}")
        traceback.print_exc()

# بدء البوت
bot.polling(none_stop=True, timeout=60)