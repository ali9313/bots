from config import *
from telebot import TeleBot, types

def load_ali_devs():
    try:
        with open('backend/ali_devs.txt', 'r', encoding='utf-8') as file:
            return file.read().splitlines()  # قراءة كل سطر كمعرف مستخدم
    except FileNotFoundError:
        return []  # في حالة عدم وجود الملف، نعيد قائمة فارغة

def dump_ali_devs(ali_devs):
    with open('backend/ali_devs.txt', 'w', encoding='utf-8') as file:
        for dev in ali_devs:
            file.write(f"{dev}\n")  # كتابة كل معرف مستخدم في سطر جديد

def load_ali_owners():
    try:
        with open('backend/ali_owners.txt', 'r', encoding='utf-8') as file:
            return file.read().splitlines()  # قراءة كل سطر كمعرف مالك
    except FileNotFoundError:
        return []  # في حالة عدم وجود الملف، نعيد قائمة فارغة

def is_owner(user_id):
    owners = load_ali_owners()
    return str(user_id) in owners  # التحقق مما إذا كان المعرف موجودًا في القائمة

def ALI(bot, a):
    # تحقق من أن المستخدم هو المطور الأساسي
    return False  # يمكن تعديلها لاحقاً حسب الحاجة

def OWNER_ID(bot, a):
    # تحقق مما إذا كان المستخدم هو المالك
    return is_owner(a.from_user.id)

def basic_dev(bot, a):
    # تحقق مما إذا كان المستخدم مطوراً ثانوياً
    return False  # يمكن تعديلها لاحقاً حسب الحاجة
def promote_devs(a):
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif len(a.text.split()) > 1:
        target = a.text.split()[1].strip("@")
        try:
            user = bot.get_chat(target)
            user_id = str(user.id)
        except:
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم أو إدخال معرفه.")
        return

    ali_devs = load_ali_devs()

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور الثانوي\n√")
        return

    if user_id in ali_devs:
        bot.reply_to(a, "◍ هذا المستخدم مطور بالفعل\n√")
    else:
        ali_devs.append(user_id)  # إضافة معرف المستخدم إلى قائمة المطورين
        dump_ali_devs(ali_devs)  # حفظ التعديلات إلى الملف
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح مطور\n√")


def get_devs(a):
    ali_devs = load_ali_devs()

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور\n√")
        return

    if not ali_devs:
        bot.reply_to(a, "لا يوجد مطورين حتى الأن")
        return

    admin_names = []
    for admin_id in ali_devs:
        try:
            user = bot.get_chat(int(admin_id))
            admin_names.append(f"[{user.first_name}](tg://user?id={user.id})")
        except:
            continue

    if admin_names:
        admin_list = "\n".join(admin_names)
        bot.reply_to(a, f"◍ قائمة المطورين:\n\n{admin_list}", parse_mode='Markdown')
    else:
        bot.reply_to(a, "تعذر العثور على معلومات المطورين")


def demote_devs(a):
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif len(a.text.split()) > 1:
        target = a.text.split()[1].strip("@")
        try:
            user = bot.get_chat(target)
            user_id = str(user.id)
        except:
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم أو إدخال معرفه.")
        return

    ali_devs = load_ali_devs()

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور الثانوي\n√")
        return

    if user_id not in ali_devs:
        bot.reply_to(a, "◍ هذا المستخدم ليس مطور لتنزيله\n√")
    else:
        ali_devs.remove(user_id)  # إزالة معرف المستخدم من قائمة المطورين
        dump_ali_devs(ali_devs)  # حفظ التعديلات إلى الملف
        bot.reply_to(a, "◍ تم تنزيل المستخدم من المطورين بنجاح\n√")


def clear_devs(a):
    ali_devs = load_ali_devs()

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور الثانوي\n√")
        return

    if ali_devs:
        ali_devs.clear()  # مسح قائمة المطورين
        dump_ali_devs(ali_devs)  # حفظ التعديلات إلى الملف
        bot.reply_to(a, "◍ تم مسح المطورين بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد مطورين ليتم مسحهم")