from config import *  # تأكد من أن mute_user و unmute_user مستوردتان من الملف المناسب
from mut import *
from rdod import *

def reply_func(a):
    try:
        user_id = a.from_user.id

        # التحقق من صلاحيات المستخدم
        if not is_authorized_user(user_id, a):
            bot.reply_to(a, "◍ أنت لست مخولًا للقيام بهذه العملية\n√")
            return

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
            mute_user(a)  # استدعاء دالة كتم المستخدم
        elif a.text in ["الغاء كتم", "الغاء لصم"]:
            unmute_user(a) 
        elif a.text == "اضف رد":
            start_adding_response(a)
        elif a.text == "حذف رد":
            start_deleting_response(a)
        elif a.text == "الردود":
            show_responses(a)

    except Exception as e:
        print(f"حدث خطأ: {e}")

# تأكد من إضافة الدالة is_authorized_user إلى الكود كما في الكود السابق.