from config import *
from telebot import types
from ali_json import *
# الوظيفة الرئيسية
def cmd(a):
    text = a.text
    msg_chat_id = a.chat.id
    msg_id = a.message_id
    user_id = a.from_user.id
    
    # استبعاد رسائل البوت نفسه
    if user_id == 6780437429:
        return
    
    # التعامل مع الأوامر
    if text == 'الاوامر':
        if not is_admin(user_id):  # تحقق من صلاحيات المستخدم
            bot.send_message(msg_chat_id, '• هذا الامر يخص { الإداريين فقط }', parse_mode="Markdown")
            return
        
        # تحقق من الاشتراك في القناة
        if not is_subscribed(user_id, msg_chat_id):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("الاشتراك", url='https://t.me/YOUR_CHANNEL'))
            bot.send_message(msg_chat_id, '• عليك الاشتراك في قناة البوت لأستخدام الاوامر', reply_markup=markup)
            return
        
        # إنشاء أزرار الاوامر
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("م1", callback_data='help1'),
                   types.InlineKeyboardButton("م2", callback_data='help2'))
        markup.row(types.InlineKeyboardButton("م3", callback_data='help3'),
                   types.InlineKeyboardButton("م4", callback_data='help4'))
        markup.row(types.InlineKeyboardButton("م المطور", callback_data='helpsudo'))
        markup.row(types.InlineKeyboardButton("قناه السورس", url='http://t.me/YOUR_CHANNEL'))

        # إرسال قائمة الأوامر
        bot.send_message(msg_chat_id, '''
        • اوامــر البــوت الرئيسيـة 
        ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉
        • { م1 } ← اوامر الحمايه
        • { م2 } ← اوامر الادمنيه
        • { م3 } ← اوامر المدراء
        • { م4 } ← اوامر المنشئين
        • { م المطور } ← اوامر المطور
        ''', parse_mode="Markdown", reply_markup=markup)
    
    elif text == 'م المطور':
        if not owner_id_ali(user_id):  # تحقق من صلاحيات المطور
            bot.send_message(msg_chat_id, '• هذا الامر يخص المطورين فقط', parse_mode="Markdown")
            return
        
        # تحقق من الاشتراك في القناة
        if not is_subscribed(user_id, msg_chat_id):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("الاشتراك", url='https://t.me/YOUR_CHANNEL'))
            bot.send_message(msg_chat_id, '• عليك الاشتراك في قناة البوت لأستخدام الاوامر', reply_markup=markup)
            return
        
        # إرسال أوامر المطور
        bot.send_message(msg_chat_id, '''
        • اوامر المطور الاساسي  
        ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉
        • تفعيل  ←  تعطيل
        • رفع  تنزيل ← مطور اساسي
        • المطورين الاساسيين
        • مسح المطورين الاساسيين
        • رفع  تنزيل ← مطور ثانوي
        • المطورين الثانويين  
        • مسح المطورين الثانويين
        • رفع  تنزيل ← مطور
        • المطورين ← مسح المطورين
        *''', parse_mode="Markdown")

# التعامل مع الضغط على الأزرار (Callback Queries)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "help1":
        bot.answer_callback_query(call.id, "عرض م1 - أوامر الحماية")
    elif call.data == "help2":
        bot.answer_callback_query(call.id, "عرض م2 - أوامر الإدمنية")
    elif call.data == "help3":
        bot.answer_callback_query(call.id, "عرض م3 - أوامر المدراء")
    elif call.data == "help4":
        bot.answer_callback_query(call.id, "عرض م4 - أوامر المنشئين")
    elif call.data == "helpsudo":
        bot.answer_callback_query(call.id, "عرض أوامر المطور")

# دالة للتحقق من صلاحيات الأدمن
def is_admin(user_id):
    # يجب إضافة منطق التحقق من الصلاحيات هنا
    return True

# دالة للتحقق من الاشتراك
def is_subscribed(user_id, chat_id):
    # منطق التحقق من الاشتراك في القناة
    return True

