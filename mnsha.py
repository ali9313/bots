from config import *
from telebot import types

# تحميل المنشئين من ملف نصي
def load_ali_creators():
    creators_dict = {"creators": {}}
    try:
        with open('backend/ali_creators.txt', 'r', encoding='utf-8') as file:
            for line in file:
                chat_id, creators = line.strip().split(':')
                creators_dict['creators'][chat_id] = {'creator_id': creators.split(',') if creators else []}
    except FileNotFoundError:
        # إذا كان الملف غير موجود، نعيد قاموس فارغ
        pass
    return creators_dict

# حفظ المنشئين في ملف نصي
def dump_ali_creators(data):
    with open('backend/ali_creators.txt', 'w', encoding='utf-8') as file:
        for chat_id, info in data['creators'].items():
            creators = ','.join(info['creator_id'])
            file.write(f"{chat_id}:{creators}\n")

def promote_creator(a):
    user_id = None
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif len(a.text.split()) > 1:
        target = a.text.split()[1]
        try:
            user = bot.get_chat_member(a.chat.id, target)
            user_id = str(user.user.id)
        except Exception:
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return
    else:
        bot.reply_to(a, "الرجاء تحديد المستخدم.")
        return

    chat_id = str(a.chat.id)
    ali_creators = load_ali_creators()

    if (not ALI(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and 
        not dev(bot, a) and not is_basic_creator(bot, a) and not owner(bot, a)):
        bot.reply_to(a, "◍ يجب ان تكون مالك حتى تستطيع رفع منشئ\n√")
        return
    
    if chat_id not in ali_creators['creators']:
        ali_creators['creators'][chat_id] = {'creator_id': []}

    if user_id in ali_creators['creators'][chat_id]['creator_id']:
        bot.reply_to(a, "◍ هذا المستخدم منشئ بالفعل\n√")
    else:
        ali_creators['creators'][chat_id]['creator_id'].append(user_id)
        dump_ali_creators(ali_creators)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح منشئ\n√")

def demote_creator(a):
    user_id = None
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif len(a.text.split()) > 1:
        target = a.text.split()[1]
        try:
            user = bot.get_chat_member(a.chat.id, target)
            user_id = str(user.user.id)
        except Exception:
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return
    else:
        bot.reply_to(a, "الرجاء تحديد المستخدم.")
        return

    chat_id = str(a.chat.id)
    ali_creators = load_ali_creators()

    if (not ALI(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and 
        not dev(bot, a) and not is_basic_creator(bot, a) and not owner(bot, a)):
        bot.reply_to(a, "◍ يجب ان تكون مالك حتى تستطيع تنزيل منشئ\n√")
        return
    
    if chat_id not in ali_creators['creators']:
        bot.reply_to(a, "لا يوجد منشئين حتى الأن")
        return

    if user_id not in ali_creators['creators'][chat_id]['creator_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس منشئ لتنزيله\n√")
    else:
        ali_creators['creators'][chat_id]['creator_id'].remove(user_id)
        dump_ali_creators(ali_creators)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من المنشئين بنجاح\n√")

def clear_creators(a):
    chat_id = str(a.chat.id)
    ali_creators = load_ali_creators()

    if (not ALI(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and 
        not dev(bot, a) and not is_basic_creator(bot, a) and not owner(bot, a)):
        bot.reply_to(a, "◍ يجب ان تكون مالك حتى تستطيع حذف المنشئين\n√")
        return
    
    if chat_id in ali_creators['creators']:
        ali_creators['creators'][chat_id]['creator_id'] = []
        dump_ali_creators(ali_creators)
        bot.reply_to(a, "◍ تم حذف المنشئين\n√")
    else:
        bot.reply_to(a, "◍ لا يوجد منشئين\n√")

def get_creators(a):
    chat_id = str(a.chat.id)
    ali_creators = load_ali_creators()

    if (not ALI(bot, a) and not basic_dev(bot, a) and not OWNER_ID(bot, a) and 
        not dev(bot, a) and not is_basic_creator(bot, a) and not owner(bot, a) and not creator(bot, a)):
        bot.reply_to(a, "◍ يجب ان تكون منشئ على الاقل لاستخدام الامر\n√")
        return

    if chat_id not in ali_creators['creators']:
        bot.reply_to(a, "◍ لا يوجد منشئين\n√")
        return
    
    admins = ali_creators['creators'][chat_id]['creator_id']
    if not admins:
        bot.reply_to(a, "◍ لا يوجد منشئين\n√")
    else:
        admin_names = []
        for admin_id in admins:
            try:
                user = bot.get_chat_member(chat_id, int(admin_id))
                admin_names.append(f"[{user.user.first_name}](tg://user?id={user.user.id})")
            except Exception:
                continue

        if admin_names:
            admin_list = "\n".join(admin_names)
            bot.reply_to(a, f"◍ قائمة المنشئين:\n\n{admin_list}", parse_mode='Markdown')
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المنشئين")