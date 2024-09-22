from config import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ترسل اهلا ارد عليك مرحبا ، ترسل غير شي ما افهم ترا")
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    if a.text=="اهلا":
          bot.reply_to(a, "مرحبا")
    else:
    	bot.reply_to(a,"لم افهمك ابدا")
    	
bot.polling()
