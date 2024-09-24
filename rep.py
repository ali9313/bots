from config import *
from insert_replyy import *
from read_replyy import *
from botcommand import *
from idee import *
from mut import *
from rtb import *
from rdod import *
def reply_func(a):
    if a.text == "اهلا":
        bot.reply_to(a, "مرحبا")
    elif a.text == "باي":
        bot.reply_to(a, "الله ياخذك")
    elif a.text == "ميكاسا":
        bot.reply_to(a,"مو عمة حد وميسي عمها")
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
    elif a.text in ["طرد", "حظر"]:
        my_cmd(a)
    elif a.text in ["كتم", "لصم"]:
    	mute_user(a)
    elif a.text == "الغاء كتم":
        unmute_user(a)
    elif a.text in ["ايدي", "ا"]:
        send_user_info(a)
    elif "رفع" in a.text:
    	promote_user(a)
    elif a.text == "رتبته":
    	read_role(a)
    elif a.text == "اضف رد":
    	start_adding_response(a)
    	else:
    		my_txtrep(a)
    else:
        my_txtrep(a)