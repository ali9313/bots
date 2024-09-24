from config import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# متغيرات لتتبع حالة المستخدم
user_states = {}
responses = {}

# اسم الملف الذي سيتم تحميل الردود منه
file_name = "backend/m_replyy.txt"  # استبدل هذا بالمسار الصحيح

# تحميل الردود المحفوظة من الملف
def load_responses():
    global responses
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            # تحقق مما إذا كان الملف فارغًا
            if f.readable() and f.read().strip() == "":
                return  # إنهاء الدالة إذا كان الملف فارغًا
            
            # العودة إلى بداية الملف
            f.seek(0)

            for line in f:
                if line.strip():
                    trigger, reply = line.strip().split(":", 1)
                    responses[trigger.strip()] = reply.strip()
    except FileNotFoundError:
        pass  # تجاهل الخطأ إذا كان الملف غير موجود

# حفظ الردود إلى الملف
def save_responses():
    with open(file_name, "w", encoding="utf-8") as f:
        for trigger, reply in responses.items():
            f.write(f"{trigger}:{reply}\n")

# دالة لحذف الردود
def start_deleting_response(a):
    keyboard = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton("إلغاء الأمر", callback_data="cancel_delete")
    keyboard.add(cancel_button)

    bot.send_message(a.chat.id, "دز كلمة الرد الي تريد احذفها ", reply_markup=keyboard)
    user_states[a.chat.id] = "awaiting_deletion"

@bot.callback_query_handler(func=lambda call: call.data == "cancel_delete")
def cancel_deletion(call):
    user_states[call.message.chat.id] = None  # إلغاء حالة المستخدم

    # تعديل نص الزر ليصبح "تم إلغاء الأمر"
    keyboard = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton("تم إلغاء الأمر", callback_data="none")
    keyboard.add(cancel_button)

    # تحديث الرسالة لتغيير الزر فقط
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_deletion")
def delete_response(a):
    trigger = a.text.strip()
    if trigger in responses:
        del responses[trigger]
        save_responses()  # حفظ التغييرات
        bot.reply_to(a, "تمام مسحنالك الرد")
        del user_states[a.chat.id]  # حذف حالة المستخدم بعد الحذف
    else:
        bot.reply_to(a, "ماكو هيج رد ولك")
        del user_states[a.chat.id]  # إلغاء حالة المستخدم

# الردود الديناميكية
@bot.message_handler(func=lambda a: a.text.strip() in responses)
def dynamic_reply(a):
    reply = responses[a.text.strip()]
    bot.reply_to(a, reply)

# دالة لجلب وعرض الردود المضافة
def show_responses(a):
    if responses:
        response_text = "**الردود المضافة:**\n"
        for trigger in responses.keys():
            response_text += f"- **{trigger}**\n"  # جلب كلمة الرد فقط
        bot.reply_to(a, response_text, parse_mode='Markdown')
    else:
        bot.reply_to(a, "لا توجد ردود مضافة حتى الآن.")

# تحميل الردود عند بدء تشغيل البوت
load_responses()