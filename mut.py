from config import *
from telebot.types import ChatPermissions

# قائمة للمستخدمين الذين سيتم حذف رسائلهم بشكل تلقائي
muted_users = set()

# الرقم الخاص برئيس الجمهورية
president_id = 232499688  # استبدل هذا الرقم برقم رئيس الجمهورية الحقيقي

@bot.message_handler(commands=['mute'])
def mute_command(a):
    mute_user(a)

@bot.message_handler(commands=['unmute'])
def unmute_command(a):
    unmute_user(a)

def mute_user(a):
    try:
        if a.reply_to_message:
            user_id = a.reply_to_message.from_user.id
            chat_id = a.chat.id
            
            # تحقق من أن المستخدم ليس رئيس الجمهورية
            if user_id == president_id:
                bot.reply_to(a, "هذا رئيس الجمهورية، محد يكدر يسكته!")
                return
            
            # تحقق إذا كان المستخدم يقوم بالرد على نفسه
            if user_id == a.from_user.id:
                bot.reply_to(a, "يا مطي تريد تكتم نفسك؟")
                return
            
            muted_users.add(user_id)
            bot.reply_to(a, f"نلصم {a.reply_to_message.from_user.first_name}")
    except Exception as e:
        bot.reply_to(a, f"حدث خطأ: {str(e)}")

def unmute_user(a):
    try:
        if a.reply_to_message:
            user_id = a.reply_to_message.from_user.id
            
            # تحقق إذا كان المستخدم يقوم بالرد على نفسه
            if user_id == a.from_user.id:
                bot.reply_to(a, "متكدر تفتح لصمك وانت اصلا مملصوم")
                return
            
            # تحقق من أن المستخدم ليس رئيس الجمهورية
            if user_id == president_id:
                bot.reply_to(a, "هذا رئيس الجمهورية، محد يكدر يسكته!")
                return
            
            if user_id in muted_users:
                muted_users.remove(user_id)
                bot.reply_to(a, f"تم إلغاء كتم {a.reply_to_message.from_user.first_name}")
            else:
                bot.reply_to(a, f"المستخدم {a.reply_to_message.from_user.first_name} غير مكتوم")
    except Exception as e:
        bot.reply_to(a, f"حدث خطأ: {str(e)}")

# إضافة معالج لحذف رسائل المستخدمين المكتمين
@bot.message_handler(func=lambda message: message.from_user.id in muted_users and message.from_user.id != president_id)
def delete_muted_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"حدث خطأ أثناء حذف الرسالة: {str(e)}")