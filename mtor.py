from config import *
from telebot import TeleBot, types
from ali_json import programmer_ali, basic_dev
import logging

# إعداد سجل الأخطاء
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def is_authorized_user(user_id, a):
    # تحقق مما إذا كان المستخدم هو مبرمج السورس أو المطور الثانوي فقط
    authorized = (
        programmer_ali(user_id) or  # التحقق من إذا كان مبرمج السورس
        basic_dev(user_id)  # التحقق من إذا كان مطورًا ثانويًا
    )
    
    logging.info(f"التحقق من الصلاحيات للمستخدم {user_id}: {'مؤهل' if authorized else 'غير مؤهل'}")
    return authorized

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

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب أن تكون مالكًا أو مطورًا لكي تستطيع رفع مستخدم.\n√")
        return

    if user_id in ali_devs:
        bot.reply_to(a, "◍ هذا المستخدم مطور بالفعل\n√")
    else:
        ali_devs.append(user_id)  # إضافة معرف المستخدم إلى قائمة المطورين
        dump_ali_devs(ali_devs)  # حفظ التعديلات إلى الملف
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح مطور\n√")

def get_devs(a):
    ali_devs = load_ali_devs()

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ انت لست المطور\n√")
        return

    if not ali_devs:
        bot.reply_to(a, "لا يوجد مطورين حتى الأن")
        return

    dev_names = []
    for dev_id in ali_devs:
        try:
            user = bot.get_chat(int(dev_id))
            dev_names.append(f"[{user.first_name}](tg://user?id={user.id})")
        except:
            continue

    if dev_names:
        dev_list = "\n".join(dev_names)
        bot.reply_to(a, f"◍ قائمة المطورين:\n\n{dev_list}", parse_mode='Markdown')
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

    if not is_authorized_user(a.from_user.id, a):
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

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ انت لست المطور الثانوي\n√")
        return

    if ali_devs:
        ali_devs.clear()  # مسح قائمة المطورين
        dump_ali_devs(ali_devs)  # حفظ التعديلات إلى الملف
        bot.reply_to(a, "◍ تم مسح المطورين بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد مطورين ليتم مسحهم")