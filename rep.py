from config import *  
from mut import *
from rdod import *
from tfael import *
from mtor import *

def reply_func(a):
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
        with open("pic/tmsah.jpg", "rb") as image:
            bot.send_photo(a.chat.id, image)
    elif a.text == "موسيقى":
        with open("voice/vv.m4a", "rb") as audio:
            bot.send_audio(a.chat.id, audio)
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
        update_owners(a)  
    elif a.text == "رفع مطور":
        promote_devs(a)
    elif a.text == "المطورين":
        get_devs(a)
    elif a.text == "تنزيل مطور":
        demote_devs(a)
    elif a.text == "مسح المطورين":
        clear_devs(a)
    elif a.text == "رفع مواطن":
        promote_distinct(a)
    elif a.text == "تنزيل مواطن":
        demote_distinct(a)
    elif a.text == "مسح المواطنين":
        clear_distinct(a)
    elif a.text == "المواطنين":
        get_distinct(a)