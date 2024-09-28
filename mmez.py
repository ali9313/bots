from config import *
import json
from telebot import TeleBot, types

# تحميل وتفريغ بيانات المميزين
def load_ali_distinct():
    try:
        with open('backend/ali_distinct.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'admin': {}}

def dump_ali_distinct(ali_distinct):
    with open('backend/ali_distinct.json', 'w') as file:
        json.dump(ali_distinct, file)

# دالة للتحقق من صلاحيات المستخدم
def is_authorized_user(user_id, a):
    return (
        ALI(bot, a) or 
        basic_dev(bot, a) or 
        OWNER_ID(bot, a) or 
        admin(bot, a) or 
        is_basic_creator(bot, a) or 
        owner(bot, a) or 
        creator(bot, a)
    )

@bot.message_handler(commands=['رفع مميز'])
def promote_distinct(a):
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ أنت لست مخولًا للقيام بهذه العملية\n√")
        return

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

    chat_id = str(a.chat.id)
    ali_distinct = load_ali_distinct()

    if chat_id not in ali_distinct['admin']:
        ali_distinct['admin'][chat_id] = {'admin_id': []}

    if user_id in ali_distinct['admin'][chat_id]['admin_id']:
        bot.reply_to(a, "◍ هذا المستخدم مميز بالفعل\n√")
    else:
        ali_distinct['admin'][chat_id]['admin_id'].append(user_id)
        dump_ali_distinct(ali_distinct)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح مميز\n√")

@bot.message_handler(commands=['تنزيل مميز'])
def demote_distinct(a):
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ أنت لست مخولًا للقيام بهذه العملية\n√")
        return

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

    chat_id = str(a.chat.id)
    ali_distinct = load_ali_distinct()

    if chat_id not in ali_distinct['admin']:
        bot.reply_to(a, "لا يوجد مميزين حتى الأن")
        return

    if user_id not in ali_distinct['admin'][chat_id]['admin_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس مميز لتنزيله\n√")
    else:
        ali_distinct['admin'][chat_id]['admin_id'].remove(user_id)
        dump_ali_distinct(ali_distinct)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من المميزين بنجاح\n√")

@bot.message_handler(commands=['مسح المميزين'])
def clear_distinct(a):
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ أنت لست مخولًا للقيام بهذه العملية\n√")
        return

    chat_id = str(a.chat.id)
    ali_distinct = load_ali_distinct()

    if chat_id in ali_distinct['admin']:
        ali_distinct['admin'][chat_id]['admin_id'] = []
        dump_ali_distinct(ali_distinct)
        bot.reply_to(a, "◍ تم مسح المميزين بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد مميزين ليتم مسحهم")

@bot.message_handler(commands=['المميزين'])
def get_distinct(a):
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ أنت لست مخولًا للقيام بهذه العملية\n√")
        return

    chat_id = str(a.chat.id)
    ali_distinct = load_ali_distinct()

    if chat_id not in ali_distinct['admin']:
        bot.reply_to(a, "لا يوجد مميزين في هذه الدردشة")
        return

    admins = ali_distinct['admin'][chat_id]['admin_id']
    if not admins:
        bot.reply_to(a, "لا يوجد مميزين في هذه الدردشة")
    else:
        admin_names = []
        for admin_id in admins:
            try:
                user = bot.get_chat(int(admin_id))
                admin_names.append(f"[{user.first_name}](tg://user?id={user.id})")
            except:
                continue

        if admin_names:
            admin_list = "\n".join(admin_names)
            bot.reply_to(a, f"◍ قائمة المميزين:\n\n{admin_list}", parse_mode='Markdown')
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المميزين")