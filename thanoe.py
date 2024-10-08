from config import *
from telebot import TeleBot, types
from ali_json import programmer_ali, owner_id_ali  # حذف استيراد basic_dev
import logging

# إعداد سجل الأخطاء
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_ali_basic_devs():
    ali_basic_devs = {'basic_devs': {}}
    try:
        with open('backend/ali_basic_devs.txt', 'r') as file:
            for line in file:
                user_id = line.strip()
                ali_basic_devs['basic_devs'][user_id] = True
    except FileNotFoundError:
        pass
    return ali_basic_devs

def dump_ali_basic_devs(ali_basic_devs):
    with open('backend/ali_basic_devs.txt', 'w') as file:
        for user_id in ali_basic_devs['basic_devs']:
            file.write(f"{user_id}\n")

# حذف التحقق من المطور الثانوي (basic_dev)
def is_authorized_user(user_id, a):
    authorized = (
        programmer_ali(user_id) or
        owner_id_ali(user_id)
    )
    
    logging.info(f"التحقق من الصلاحيات للمستخدم {user_id}: {'مؤهل' if authorized else 'غير مؤهل'}")
    return authorized

def promote_basic_dev(a):
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

    ali_basic_devs = load_ali_basic_devs()

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ هذا الامر خاص بالمطور الاساسي\n√")
    elif user_id in ali_basic_devs['basic_devs']:
        bot.reply_to(a, "◍ هذا المستخدم مطور ثانوي بالفعل\n√")
    else:
        ali_basic_devs['basic_devs'][user_id] = True
        dump_ali_basic_devs(ali_basic_devs)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح مطور ثانوي\n√")

def list_basic_devs(a):
    ali_basic_devs = load_ali_basic_devs()

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ هذا الامر خاص بالمطور الاساسي\n√")
        return

    basic_devs = ali_basic_devs['basic_devs']
    if not basic_devs:
        bot.reply_to(a, "لا يوجد مطورين ثانويين")
    else:
        basic_dev_names = []
        for basic_dev_id in basic_devs:
            try:
                user = bot.get_chat(int(basic_dev_id))
                basic_dev_names.append(f"[{user.first_name}](tg://user?id={user.id})")
            except:
                continue

        if basic_dev_names:
            basic_dev_list = "\n".join(basic_dev_names)
            bot.reply_to(a, f"◍ قائمة الثانويين:\n\n{basic_dev_list}", parse_mode='Markdown')
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المطورين الثانويين")

def demote_basic_dev(a):
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

    ali_basic_devs = load_ali_basic_devs()

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ هذا الامر خاص بالمطور الاساسي\n√")
        return

    if user_id not in ali_basic_devs['basic_devs']:
        bot.reply_to(a, "◍ هذا المستخدم ليس ثانويا لتنزيله\n√")
    else:
        del ali_basic_devs['basic_devs'][user_id]
        dump_ali_basic_devs(ali_basic_devs)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من الثانويين بنجاح\n√")

def clear_basic_devs(a):
    ali_basic_devs = load_ali_basic_devs()

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ هذا الامر خاص بالمطور الاساسي\n√")
        return

    ali_basic_devs['basic_devs'] = {}
    dump_ali_basic_devs(ali_basic_devs)
    bot.reply_to(a, "◍ تم مسح الثانويين بنجاح\n√")