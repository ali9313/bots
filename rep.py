from config import *
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
    else:
        bot.reply_to(a, "طيطي")