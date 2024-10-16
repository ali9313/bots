import logging
from config import *
from mut import *
from rdod import *
from tfael import *
from mtor import *
from mmez import *
from malk import *
from mnsha import *
from mnshaas import *
from thanoe import *
from admin import *
from translate import *
from sond import *
from ttt import *

# إعداد السجلات (Logging)
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def reply_func(a):
    try:
        logging.info(f"Received message: {a.text} from user {a.from_user.id} in chat {a.chat.id}")
        print(f"Received message: {a.text}")  # تتبع الرسائل الواردة
        
        if a.text == "اهلا":
            bot.reply_to(a, "مرحبا")
        elif a.text == "باي":
            bot.reply_to(a, "الله ياخذك")
        elif a.text == "ميكاسا":
            bot.reply_to(a, "مو عمة حد وميسي عمها")
        elif a.text == "ملاك":
            bot.reply_to(a, """͏
                              ╱|、
                             (˚ˎ 。7  
                              |、˜〵          
                             じしˍ,)ノ""")
        elif "تمساح" in a.text:
            bot.reply_to(a, "يبحث عن ثلاثينية")
        elif a.text == "بوت":
            bot.reply_to(a, "ها شتريد")
        elif a.text == "تمسوح":
            try:
                with open("pic/tmsah.jpg", "rb") as image:
                    bot.send_photo(a.chat.id, image)
            except FileNotFoundError:
                logging.error("تمسوح image file not found.")
                bot.reply_to(a, "الصورة غير موجودة.")
        elif a.text == "موسيقى":
            try:
                with open("voice/vv.m4a", "rb") as audio:
                    bot.send_audio(a.chat.id, audio)
            except FileNotFoundError:
                logging.error("موسيقى audio file not found.")
                bot.reply_to(a, "الملف الصوتي غير موجود.")
        elif a.text in ["كتم", "لصم"]:
            mute_user(a)
        elif a.text in ["الغاء كتم", "الغاء لصم"]:
            unmute_user(a)
        elif a.text == "اضف رد":
            start_adding_response(a)
        elif a.text == "حذف رد":
            start_deleting_response(a)
        elif a.text == "الردود":
            show_responses(a)
        elif a.text == "تفعيل":
            update_admins_and_owner(a)
        elif a.text == "رفع مطور":
            promote_devs(a)
        elif a.text == "المطورين":
            get_devs(a)
        elif a.text == "تنزيل مطور":
            demote_devs(a)
        elif a.text == "مسح المطورين":
            clear_devs(a)
        elif a.text == "رفع مواطن":
            add_distinct(a)
        elif a.text == "تنزيل مواطن":
            remove_distinct(a)
        elif a.text == "مسح المواطنين":
            clear_distinct(a)
        elif a.text == "المواطنين":
            get_distinct(a)
        elif a.text == "رفع مالك":
            promote_owner(a)
        elif a.text == "تنزيل مالك":
            demote_owner(a)
        elif a.text == "مسح المالكين":
            clear_owner(a)
        elif a.text == "المالكين":
            get_owner(a)
        elif a.text == "رفع منشئ":
            promote_creator(a)
        elif a.text == "تنزيل منشئ":
            demote_creator(a)
        elif a.text == "مسح المنشئين":
            clear_creators(a)
        elif a.text == "المنشئين":
            get_creators(a)
        elif a.text == "رفع منشئ اساسي":
            promote_basic_creator(a)
        elif a.text == "تنزيل منشئ اساسي":
            demote_basic_creator(a)
        elif a.text == "المنشئين الاساسيين":
            get_basic_creators(a)
        elif a.text == "مسح المنشئين الاساسيين":
            clear_basic_creators(a)
        elif a.text == "رفع ثانوي":
            promote_basic_dev(a)
        elif a.text == "الثانويين":
            list_basic_devs(a)
        elif a.text == "تنزيل ثانوي":
            demote_basic_dev(a)
        elif a.text == "مسح الثانويين":
            clear_basic_devs(a)
        elif a.text == "رفع مشرف":
            promote_admin(a)
        elif a.text == "تنزيل مشرف":
            demote_admin(a)
        elif a.text == "مسح المشرفين":
            clear_admins(a)
        elif a.text == "المشرفين":
            get_admins(a)
        elif a.text in ["ا","ايدي"]:
            send_user_info_with_photo(a)
        elif a.text == "صورته":
            send_user_photo(a)
        elif a.text == "لعربي":
            handle_translation(a)
        elif a.text == "لصوت":
            handle_message(a)
        elif a.text == "لنص":
            handle_voice_message(a)
        elif a.text == "تغ":
            send_template_options(a)
            
    except Exception as e:
        logging.error(f"Error in reply_func: {e}, user_id: {a.from_user.id}, chat_id: {a.chat.id}")
        bot.reply_to(a, "حدث خطأ أثناء تنفيذ الطلب.")