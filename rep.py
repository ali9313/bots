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
    elif a.text == "بوت":
        bot.reply_to(a, "ها شتريد")
    elif a.text == "طرد" or a.text == "حظر":
		bnn=bot.ban_chat_member(a.chat.id,a.reply_to_message.from_user.id)
	if bnn:
			bot.send_message(a.chat.id, "تم دفر: @" + a.reply_to_message.from_user.username)
   