from config import *
import json
from telebot import TeleBot, types

# تحميل وتفريغ بيانات المالكين
def load_ali_owners():
    try:
        with open('backend/ali_owners.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'owners': {}}

def dump_ali_owners(ali_owners):
    with open('backend/ali_owners.json', 'w') as file:
        json.dump(ali_owners, file)

@bot.message_handler(commands=['رفع مالك'])
def promote_owner(a):
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
    ali_owners = load_ali_owners()

    if (not ALI(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and 
        not dev(bot, a) and not is_basic_creator(bot, a)):
        bot.reply_to(a, "◍ انت لست المنشئ الاساسي\n√")
        return

    if chat_id not in ali_owners['owners']:
        ali_owners['owners'][chat_id] = {'owner_id': []}

    if user_id in ali_owners['owners'][chat_id]['owner_id']:
        bot.reply_to(a, "◍ هذا المستخدم مالك بالفعل\n√")
    else:
        ali_owners['owners'][chat_id]['owner_id'].append(user_id)
        dump_ali_owners(ali_owners)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح مالك\n√")

@bot.message_handler(commands=['تنزيل مالك'])
def demote_owner(a):
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
    ali_owners = load_ali_owners()

    if (not ALI(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and 
        not dev(bot, a) and not is_basic_creator(bot, a)):
        bot.reply_to(a, "◍ انت لست المنشئ الاساسي\n√")
        return

    if chat_id not in ali_owners['owners']:
        bot.reply_to(a, "لا يوجد مالكين في هذه الدردشة حتى الأن")
        return

    if user_id not in ali_owners['owners'][chat_id]['owner_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس مالك لتنزيله\n√")
    else:
        ali_owners['owners'][chat_id]['owner_id'].remove(user_id)
        dump_ali_owners(ali_owners)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من المالكين بنجاح\n√")

@bot.message_handler(commands=['مسح المالكين'])
def clear_owner(a):
    chat_id = str(a.chat.id)
    ali_owners = load_ali_owners()

    if (not ALI(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and 
        not dev(bot, a) and not is_basic_creator(bot, a)):
        bot.reply_to(a, "◍ انت لست المنشئ الاساسي\n√")
        return

    if chat_id in ali_owners['owners']:
        ali_owners['owners'][chat_id]['owner_id'] = []
        dump_ali_owners(ali_owners)
        bot.reply_to(a, "◍ تم مسح المالكين بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد مالكين ليتم مسحهم")

@bot.message_handler(commands=['المالكين'])
def get_owner(a):
    chat_id = str(a.chat.id)
    ali_owners = load_ali_owners()

    if (not ALI(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and 
        not dev(bot, a) and not is_basic_creator(bot, a)):
        bot.reply_to(a, "◍ يجب ان تكون مالك على الاقل لستخدام الامر\n√")
        return

    if chat_id not in ali_owners['owners']:
        bot.reply_to(a, "لا يوجد مالكين حتى الأن")
        return

    owners = ali_owners['owners'][chat_id]['owner_id']
    if not owners:
        bot.reply_to(a, "لا يوجد مالكين حتى الأن")
    else:
        owner_names = []
        for owner_id in owners:
            try:
                user = bot.get_chat(owner_id)
                owner_names.append(f"[{user.first_name}](tg://user?id={user.id})")
            except:
                continue

        if owner_names:
            owner_list = "\n".join(owner_names)
            bot.reply_to(a, f"◍ قائمة المالكين:\n\n{owner_list}", parse_mode='Markdown')
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المالكين")