from config import *
from insert_replyy import *
from read_replyy import *
from botcommand import *

def reply_func(a):
    if a.text == "اهلا":
        bot.reply_to(a, "مرحبا")
    elif a.text == "باي":
        bot.reply_to(a, "الله ياخذك")
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
        bot.reply_to(a, open("pic/tmsah.jpg", "rb"))
    elif a.text == "موسيقى":
        bot.reply_to(a, open("voice/vv.m4a", "rb"))
    elif a.text == "طرد" or a.text == "حظر":
        my_cmd(a)
    elif "اضف" in a.text:
        insert_rep(a)
    else:
        my_txtrep(a)