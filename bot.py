from config import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! كيف يمكنني مساعدتك؟")

@bot.message_handler(func=lambda a: True)
def echo_message(message):
    if a.text=="اهلا":
          bot.reply_to(a, "مرحبا")
    else:
    	bot.reply_to(a,"لم افهمك ابدا")
    	
bot.polling()
