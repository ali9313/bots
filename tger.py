from config import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# دالة لإنشاء الأزرار التفاعلية
def generate_confirmation_buttons():
    markup = InlineKeyboardMarkup()
    confirm_button = InlineKeyboardButton("تأكيد", callback_data="confirm")
    skip_button = InlineKeyboardButton("تخطي", callback_data="skip")
    markup.add(confirm_button, skip_button)
    return markup

# دالة لإنشاء الرسالة المخصصة
def generate_custom_message(user_id, username, msgs):
    message_template = """
    ✧ : المستخدم 𓅫 
    ✧ : هل تريد تعيين هذه الكليشه للايدي :

    ⌜
    ◇ : Msgs : {msgs} .
    ◇ : ID : {id} .
    ◇ : Username : {username} .
    ⌟
    """
    return message_template.format(id=user_id, username=username, msgs=msgs)

# دالة لمعالجة بدء المحادثة
def start_message(a):
    user_id = a.from_user.id
    username = a.from_user.username if a.from_user.username else "لا يـوجـد"
    msgs = 123  # يمكن استبدال هذا بعدد الرسائل الحقيقي
    
    # إنشاء الرسالة
    custom_message = generate_custom_message(user_id, username, msgs)
    
    # إرسال الرسالة مع الأزرار التفاعلية
    bot.send_message(a.chat.id, custom_message, reply_markup=generate_confirmation_buttons())


def handle_query(a):
    if a.data == "confirm":
        bot.send_message(a.message.chat.id, "تم تأكيد الكليشه!")
    elif a.data == "skip":
        bot.send_message(a.message.chat.id, "تم تخطي الكليشه!")
