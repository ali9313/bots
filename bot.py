from config import *
from rep import *
from botcommand import *
from telegram.ext import Updater, CommandHandler

# تعريف المتغيرات
updater = Updater(TOKEN)  # تأكد من أن TOKEN معرف بشكل صحيح
dispatcher = updater.dispatcher

@bot.message_handler(content_types=['new_chat_members', 'left_chat_members'])
def cmbr(a):
    bot.delete_message(a.chat.id, a.message_id)

@bot.message_handler(commands=['start', 'ban'])
def my(a):
    # منطق دالة /ban يمكن أن يضاف هنا
    pass

def send_welcome(message):
    bot.reply_to(message, "ترسل اهلا ارد عليك مرحبا ، ترسل غير شي ما افهم ترا")

@bot.message_handler(func=lambda a: True)
def echo_message(a):
    reply_func(a)  # تأكد من أن reply_func معرفة

# إضافة معالج للأمر "/ban"
dispatcher.add_handler(CommandHandler('ban', my))

# بدء تشغيل البوت
updater.start_polling()
updater.idle()