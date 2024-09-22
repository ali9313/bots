from config import *
from rep import *
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ترسل اهلا ارد عليك مرحبا ، ترسل غير شي ما افهم ترا")

@bot.message_handler(func=lambda a: True)
def echo_message(a):
    reply_func(a)

bot.polling()