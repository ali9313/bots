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
# معالج الرسائل العامة
@bot.message_handler(func=lambda a: True)
def echo_message(a):
            reply_func(a)  
bot.polling(none_stop=True)