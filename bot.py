from config import *
from rep import *
from botcommand import *
@bot.message_handler(content_types=['new_chat_members', 'left_chat_members'])
def cmbr(a):
    bot.delete_message(a.chat.id, a.message_id)

@bot.message_handler(commands=['start', 'ban'])
def my(a):
    if a.text == "/ban" and a.reply_to_message:
        # منطق الحظر يمكن أن يضاف هنا
        my_cmd(a)
    else:
        send_welcome(a)

def send_welcome(a):
    bot.reply_to(a, "ترسل اهلا ارد عليك مرحبا ، ترسل غير شي ما افهم ترا")

@bot.message_handler(func=lambda a: True)
def echo_message(a):
    reply_func(a)  # تأكد من أن reply_func معرفة

# بدء تشغيل البوت
bot.polling()