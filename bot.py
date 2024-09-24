from config import *
from rep import *
from botcommand import *
from mut import *
@bot.message_handler(content_types=['new_chat_members', 'left_chat_members'])
def cmbr(a):
    bot.delete_message(a.chat.id, a.message_id)

@bot.message_handler(commands=['start', 'ban'])
def my(a):
    if a.text == "/ban" and a.reply_to_message:
        my_cmd(a)
    else:
        send_welcome(a)

def send_welcome(a):
    bot.reply_to(a, "ترسل اهلا ارد عليك مرحبا ، ترسل غير شي ما افهم ترا")

@bot.message_handler(func=lambda a: True)
def echo_message(a):
    reply_func(a) 
@bot.message_handler(func=lambda a: a.from_user.id in muted_users)
def delete_muted_message(a):
    try:
        bot.delete_message(a.chat.id, a.message_id)
    except Exception as e:
        bot.reply_to(a, f"حدث خطأ عند محاولة حذف الرسالة: {str(e)}")
bot.polling()