from config import *

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

def start_adding_response(a):
    bot.reply_to(a, "أهلاً عزيزي! أرسل الآن كلمة الرد.")
    user_states[a.chat.id] = "awaiting_trigger"

# استقبال كلمة الرد
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "awaiting_trigger")
def get_trigger(a):
    user_states[a.chat.id] = "awaiting_reply"
    responses[a.chat.id] = {"trigger": a.text.strip()}
    bot.reply_to(a, "الآن قم بإرسال جواب الرد الذي تريده.")

# استقبال جواب الرد
@bot.message_handler(func=lambda a: user_states.get(a.chat.id) == "awaiting_reply")
def get_reply(a):
    trigger = responses[a.chat.id]["trigger"]
    reply = a.text.strip()
    responses[trigger] = reply
    save_responses()  # حفظ الردود الجديدة
    bot.reply_to(a, "تم إضافة الرد بنجاح!")
    del user_states[a.chat.id]
    del responses[a.chat.id]

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

def handle_show_responses(a):
    show_responses(a)

# تحميل الردود عند بدء تشغيل البوت
load_responses()