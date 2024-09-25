from config import *  # تأكد من أن mute_user و unmute_user مستوردتان من الملف المناسب
from mut import *
from rtb import *

def reply_func(a):
    # التحقق مما إذا كانت الجملة تبدأ بكلمة "رفع"
    if a.text.startswith("رفع "):
        promote_user(a)  # استدعاء دالة رفع الرتبة

    elif a.text == "اهلا":
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
        mute_user(a)  # استدعاء دالة كتم المستخدم
    elif a.text in ["الغاء كتم", "الغاء لصم"]:
        unmute_user(a)  # استدعاء دالة إلغاء كتم المستخدم
    elif a.text == "رتبته":
        check_user_role(a)
    elif a.text == "رتبتي":
    	check_sender_role(a)
    elif a.text in ["ايدي", "ا"]:
    	send_user_info(a)
    elif a.text == "تنزيل":
    	demote_user(a)