from config import *
import json
from telebot import TeleBot, types
def load_ali_devs():
    try:
        with open('backend/ali_devs.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'devs': {}}

def dump_ali_devs(ali_devs):
    with open('backend/ali_devs.json', 'w') as file:
        json.dump(ali_devs, file)

def ALI(bot, a):
    # تحقق من أن المستخدم هو المطور الأساسي
    return False

def OWNER_ID(bot, a):
    # تحقق من أن المستخدم هو المالك
    return False

def basic_dev(bot, a):
    # تحقق مما إذا كان المستخدم مطوراً ثانوياً
    return False

@bot.message_handler(commands=['رفع مطور'])
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

    if user_id in ali_devs['devs']:
        bot.reply_to(a, "◍ هذا المستخدم مطور بالفعل\n√")
    else:
        ali_devs['devs'][user_id] = True
        dump_ali_devs(ali_devs)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح مطور\n√")

@bot.message_handler(commands=['المطورين'])
def get_devs(a):
    ali_devs = load_ali_devs()

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور\n√")
        return

    if 'devs' not in ali_devs or not ali_devs['devs']:
        bot.reply_to(a, "لا يوجد مطورين حتى الأن")
        return

    admin_names = []
    for admin_id in ali_devs['devs']:
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

@bot.message_handler(commands=['تنزيل مطور'])
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

    if user_id not in ali_devs['devs']:
        bot.reply_to(a, "◍ هذا المستخدم ليس مطور لتنزيله\n√")
    else:
        del ali_devs['devs'][user_id]
        dump_ali_devs(ali_devs)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من المطورين بنجاح\n√")

@bot.message_handler(commands=['مسح المطورين'])
def clear_devs(a):
    ali_devs = load_ali_devs()

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور الثانوي\n√")
        return

    if 'devs' in ali_devs and ali_devs['devs']:
        ali_devs['devs'] = {}
        dump_ali_devs(ali_devs)
        bot.reply_to(a, "◍ تم مسح المطورين بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد مطورين ليتم مسحهم")