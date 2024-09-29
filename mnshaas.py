from config import *
from telebot import types

# تحميل بيانات المنشئين الأساسيين من ملف نصي
def load_ali_basic_creators():
    try:
        with open('backend/ali_basic_creators.txt', 'r') as file:
            lines = file.readlines()
            return {'basic_creators': {line.strip(): True for line in lines}}
    except FileNotFoundError:
        return {'basic_creators': {}}

# حفظ بيانات المنشئين الأساسيين إلى ملف نصي
def dump_ali_basic_creators(data):
    with open('backend/ali_basic_creators.txt', 'w') as file:
        for user_id in data['basic_creators']:
            file.write(f"{user_id}\n")

def is_authorized_user(user_id, a):
    return (
        ALI(user_id, a) or 
        basic_dev(user_id, a) or 
        OWNER_ID(user_id, a) or 
        dev(user_id, a)
    )

def promote_basic_creator(a):
    user_id = None
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif len(a.text.split()) > 1:
        target = a.text.split()[1].strip("@")
        try:
            user = bot.get_chat_member(a.chat.id, target)
            user_id = str(user.user.id)
        except:
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ انت لست المطور\n√")
        return

    ali_basic_creators = load_ali_basic_creators()

    if user_id in ali_basic_creators['basic_creators']:
        bot.reply_to(a, "◍ هذا المستخدم منشئ اساسي بالفعل\n√")
    else:
        ali_basic_creators['basic_creators'][user_id] = True
        dump_ali_basic_creators(ali_basic_creators)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح منشئ اساسي\n√")

def demote_basic_creator(a):
    user_id = None
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif len(a.text.split()) > 1:
        target = a.text.split()[1].strip("@")
        try:
            user = bot.get_chat_member(a.chat.id, target)
            user_id = str(user.user.id)
        except:
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ انت لست المطور\n√")
        return

    ali_basic_creators = load_ali_basic_creators()

    if user_id not in ali_basic_creators['basic_creators']:
        bot.reply_to(a, "◍ هذا المستخدم ليس منشئ اساسي لتنزيله\n√")
    else:
        del ali_basic_creators['basic_creators'][user_id]
        dump_ali_basic_creators(ali_basic_creators)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من المنشئين الاساسيين بنجاح\n√")

def get_basic_creators(a):
    ali_basic_creators = load_ali_basic_creators()
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ انت لست المنشئ الاساسي\n√")
        return

    if 'basic_creators' not in ali_basic_creators:
        bot.reply_to(a, "لا يوجد منشئين اساسيين حتى الأن")
        return

    basic_creators = ali_basic_creators['basic_creators']
    if not basic_creators:
        bot.reply_to(a, "لا يوجد منشئين اساسيين حتى الأن")
    else:
        creator_names = []
        for creator_id in basic_creators:
            try:
                user = bot.get_chat(int(creator_id))
                if user:
                    creator_names.append(f"[{user.first_name}](tg://user?id={user.id})")
            except:
                continue

        if creator_names:
            creator_list = "\n".join(creator_names)
            bot.reply_to(a, f"◍ قائمة المنشئين الاساسيين:\n\n{creator_list}")
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المنشئين الاساسيين")

def clear_basic_creators(a):
    ali_basic_creators = load_ali_basic_creators()
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ انت لست المطور\n√")
        return

    if 'basic_creators' in ali_basic_creators:
        ali_basic_creators['basic_creators'] = {}
        dump_ali_basic_creators(ali_basic_creators)
        bot.reply_to(a, "◍ تم مسح المنشئين الاساسيين بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد منشئين اساسيين ليتم مسحهم")