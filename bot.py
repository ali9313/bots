from config import *
from rep import *
from botcommand import *
from mut import *
from rdod import load_responses  # استيراد دالة تحميل الردود

@bot.message_handler(content_types=['new_chat_members', 'left_chat_members'])
def cmbr(a):
    try:
        bot.delete_message(a.chat.id, a.message_id)
    except Exception as e:
        print(f"Error in 'cmbr' function: {str(e)}")
        bot.reply_to(a, f"حدث خطأ عند محاولة حذف الرسالة: {str(e)}")

@bot.message_handler(commands=['start', 'ban'])
def my(a):
    try:
        if a.text == "/ban" and a.reply_to_message:
            my_cmd(a)
        else:
            send_welcome(a)
    except Exception as e:
        print(f"Error in 'my' function: {str(e)}")
        bot.reply_to(a, f"حدث خطأ في تنفيذ الأمر: {str(e)}")

def send_welcome(a):
    try:
        bot.reply_to(a, "ترسل اهلا ارد عليك مرحبا ، ترسل غير شي ما افهم ترا")
    except Exception as e:
        print(f"Error in 'send_welcome' function: {str(e)}")
        bot.reply_to(a, f"حدث خطأ عند محاولة الرد: {str(e)}")

# معالج حذف الرسائل للمستخدمين المكتمين
@bot.message_handler(func=lambda a: a.from_user.id in muted_users)
def delete_muted_message(a):
    try:
        bot.delete_message(a.chat.id, a.message_id)
    except Exception as e:
        print(f"Error in 'delete_muted_message' function: {str(e)}")
        bot.reply_to(a, f"حدث خطأ عند محاولة حذف الرسالة: {str(e)}")

# معالج الرسائل العامة (يجب أن يأتي بعد معالج حذف الرسائل)
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        reply_func(a)
    except Exception as e:
        print(f"Error in 'echo_message' function: {str(e)}")
        bot.reply_to(a, f"حدث خطأ في معالجة الرسالة: {str(e)}")

# بدء تشغيل البوت
bot.polling()