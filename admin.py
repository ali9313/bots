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
            a.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        a.reply_text("يرجى الرد على رسالة المستخدم أو إدخال معرفه.")
        return

    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if (not Ali(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and not dev(bot, a) and not is_basic_creator(bot, a) and not owner(bot, a) and not creator(bot, a)):
        a.reply_text("◍ يجب ان تكون منشئ على الاقل لكى تستطيع رفع ادمن\n√")
        return

    if chat_id not in ali_admin['admin']:
        ali_admin['admin'][chat_id] = {'admin_id': []}

    if user_id in ali_admin['admin'][chat_id]['admin_id']:
        a.reply_text("◍ هذا المستخدم ادمن بالفعل\n√")
    else:
        ali_admin['admin'][chat_id]['admin_id'].append(user_id)
        dump_ali_admin(ali_admin)
        a.reply_text("◍ تم رفع المستخدم ليصبح ادمن\n√")

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
            a.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        a.reply_text("يرجى الرد على رسالة المستخدم أو إدخال معرفه.")
        return

    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if (not Ali(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and not dev(bot, a) and not is_basic_creator(bot, a) and not owner(bot, a) and not creator(bot, a)):
        a.reply_text("◍ يجب ان تكون منشئ على الاقل لكى تستطيع تنزيل ادمن\n√")
        return

    if chat_id not in ali_admin['admin']:
        a.reply_text("لا يوجد مشرفين حتى الأن")
        return

    if user_id not in ali_admin['admin'][chat_id]['admin_id']:
        a.reply_text("◍ هذا المستخدم ليس ادمن لتنزيله\n√")
    else:
        ali_admin['admin'][chat_id]['admin_id'].remove(user_id)
        dump_ali_admin(ali_admin)
        a.reply_text("◍ تم تنزيل المستخدم من الادمن بنجاح\n√")

@bot.message_handler(commands=['مسح الادمنيه'])
def clear_admins(a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if (not Ali(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and not dev(bot, a) and not is_basic_creator(bot, a) and not owner(bot, a) and not creator(bot, a)):
        a.reply_text("◍ يجب ان تكون منشئ على الاقل لستخدام الامر\n√")
        return

    if chat_id in ali_admin['admin']:
        ali_admin['admin'][chat_id]['admin_id'] = []
        dump_ali_admin(ali_admin)
        a.reply_text("◍ تم مسح الادمنيه بنجاح\n√")
    else:
        a.reply_text("لا يوجد ادمنيه ليتم مسحهم")

@bot.message_handler(commands=['الادمنيه'])
def get_admins(a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if chat_id not in ali_admin['admin']:
        a.reply_text("لا يوجد مشرفين في هذه الدردشة")
        return

    admins = ali_admin['admin'][chat_id]['admin_id']
    if not admins:
        a.reply_text("لا يوجد مشرفين في هذه الدردشة")
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
            a.reply_text(f"◍ قائمة المشرفين:\n\n{admin_list}", parse_mode='Markdown')
        else:
            a.reply_text("تعذر العثور على معلومات المشرفين")