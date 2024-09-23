from config import *
from rep import *
from botcommand import *
@bot.message_handler(content_types=['new_chat_members','left_chat_members'])
def cmbr(a):
	bot.delete_message(a.chat.id,a.message_id)
@bot.message_handler(commands=['start','ban'])
def my(a):
	updater = Updater(took, use_context=True)
    dp = updater.dispatche
	my_cmd(a: Update, context: CallbackContext)
def send_welcome(message):
    bot.reply_to(message, "ترسل اهلا ارد عليك مرحبا ، ترسل غير شي ما افهم ترا")
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    reply_func(a)

bot.polling()
bot.idle()

