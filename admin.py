from config import *
import json
from telebot import TeleBot, types

# تحميل وتفريغ بيانات المدراء
def load_ali_admin():
    try:
        with open('backend/ali_admin.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'admin': {}}

def dump_ali_admin(ali_admin):
    with open('backend/ali_admin.json', 'w') as file:
        json.dump(ali_admin, file)

@bot.message_handler(commands=['رفع ادمن'])
def promote_admin(a):
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
    ali_admin = load_ali_admin()

    if not is_authorized_user(a.from_user.id, a):  # استخدام الدالة من ملف main
        bot.reply_to(a, "◍ يجب ان تكون منشئ على الاقل لكى تستطيع رفع ادمن\n√")
        return

    if chat_id not in ali_admin['admin']:
        ali_admin['admin'][chat_id] = {'admin_id': []}

    if user_id in ali_admin['admin'][chat_id]['admin_id']:
        bot.reply_to(a, "◍ هذا المستخدم ادمن بالفعل\n√")
    else:
        ali_admin['admin'][chat_id]['admin_id'].append(user_id)
        dump_ali_admin(ali_admin)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح ادمن\n√")

@bot.message_handler(commands=['تنزيل ادمن'])
def demote_admin(a):
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
    ali_admin = load_ali_admin()

    if not is_authorized_user(a.from_user.id, a):  # استخدام الدالة من ملف main
        bot.reply_to(a, "◍ يجب ان تكون منشئ على الاقل لكى تستطيع تنزيل ادمن\n√")
        return

    if chat_id not in ali_admin['admin']:
        bot.reply_to(a, "لا يوجد مشرفين حتى الأن")
        return

    if user_id not in ali_admin['admin'][chat_id]['admin_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس ادمن لتنزيله\n√")
    else:
        ali_admin['admin'][chat_id]['admin_id'].remove(user_id)
        dump_ali_admin(ali_admin)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من الادمن بنجاح\n√")

@bot.message_handler(commands=['مسح الادمنيه'])
def clear_admins(a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if not is_authorized_user(a.from_user.id, a):  # استخدام الدالة من ملف main
        bot.reply_to(a, "◍ يجب ان تكون منشئ على الاقل لاستخدام الامر\n√")
        return

    if chat_id in ali_admin['admin']:
        ali_admin['admin'][chat_id]['admin_id'] = []
        dump_ali_admin(ali_admin)
        bot.reply_to(a, "◍ تم مسح الادمنيه بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد ادمنيه ليتم مسحهم")

@bot.message_handler(commands=['الادمنيه'])
def get_admins(a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if chat_id not in ali_admin['admin']:
        bot.reply_to(a, "لا يوجد مشرفين في هذه الدردشة")
        return

    admins = ali_admin['admin'][chat_id]['admin_id']
    if not admins:
        bot.reply_to(a, "لا يوجد مشرفين في هذه الدردشة")
    else:
        admin_names = []
        for admin_id in admins:
            try:
                user = bot.get_chat_member(chat_id, admin_id).user
                admin_names.append(f"[{user.first_name}](tg://user?id={user.id})")
            except:
                continue

        if admin_names:
            admin_list = "\n".join(admin_names)
            bot.reply_to(a, f"◍ قائمة المشرفين:\n\n{admin_list}", parse_mode='Markdown')
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المشرفين")