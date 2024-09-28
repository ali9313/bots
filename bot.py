from config import *
from rep import *
from admin import *  # استيراد الملف الذي يحتوي على دوال مميزين
from ali_json import *    # استيراد الملف الذي يحتوي على دوال المنشئين
from malk import *
from mmez import *
from mnsha import *
from mnshaas import *
from mtor import *
from tfael import *
from thanoe import *
def is_authorized_user(user_id, a):
    return (
        ALI(user_id, a) or 
        basic_dev(user_id, a) or 
        OWNER_ID(user_id, a) or 
        dev(user_id, a)
    )

# معالج الرسائل العامة
@bot.message_handler(func=lambda a: True)
def echo_message(a):
    try:
        if is_authorized_user(a.from_user.id, a):
            reply_func(a)  # استدعاء الدالة فقط إذا كان المستخدم مخولًا
        else:
            bot.reply_to(a, "◍ أنت لست مخولًا للقيام بهذه العملية\n√")
    except Exception as e:
        print(f"Error in 'echo_message' function: {str(e)}")
        bot.reply_to(a, f"حدث خطأ في معالجة الرسالة: {str(e)}")

# بدء تشغيل البوت
bot.polling(none_stop=True)