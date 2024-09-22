from config import *
bot = telebot.TeleBot(TOKEN)

def reply_func(a):
    if a.text == "اهلا":
        bot.reply_to(a, "مرحبا")
    elif a.text == "باي":
        bot.reply_to(a, "الله ياخذك")
    elif a.text == "ملاك":
        bot.reply_to(a, "القطة")
    elif "تمساح" in a.text:
        bot.reply_to(a, "يبحث عن ثلاثينية")
    else:
        bot.reply_to(a, "لم افهمك ابدا")