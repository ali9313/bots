from config import *
import json
from telebot import TeleBot, types
def load_ali_basic_devs():
    try:
        with open('backend/ali_basic_devs.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'basic_devs': {}}

def dump_ali_basic_devs(ali_basic_devs):
    with open('backend/ali_basic_devs.json', 'w') as file:
        json.dump(ali_basic_devs, file)

@bot.message_handler(commands=['رفع ثانوي'])
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

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور الاساسي\n√")
    elif user_id in ali_basic_devs['basic_devs']:
        bot.reply_to(a, "◍ هذا المستخدم مطور ثانوي بالفعل\n√")
    else:
        ali_basic_devs['basic_devs'][user_id] = True
        dump_ali_basic_devs(ali_basic_devs)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح مطور ثانوي\n√")

@bot.message_handler(commands=['الثانويين'])
def list_basic_devs(a):
    ali_basic_devs = load_ali_basic_devs()

    if not (ALI(bot, a) or basic_dev(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور الثانوي\n√")
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

@bot.message_handler(commands=['تنزيل ثانوي'])
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

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور الاساسي\n√")
        return

    if user_id not in ali_basic_devs['basic_devs']:
        bot.reply_to(a, "◍ هذا المستخدم ليس ثانويا لتنزيله\n√")
    else:
        del ali_basic_devs['basic_devs'][user_id]
        dump_ali_basic_devs(ali_basic_devs)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من الثانويين بنجاح\n√")

@bot.message_handler(commands=['مسح الثانويين'])
def clear_basic_devs(a):
    ali_basic_devs = load_ali_basic_devs()

    if not (ALI(bot, a) or OWNER_ID(bot, a)):
        bot.reply_to(a, "◍ انت لست المطور الاساسي\n√")
        return

    if 'basic_devs' in ali_basic_devs:
        ali_basic_devs['basic_devs'] = {}
        dump_ali_basic_devs(ali_basic_devs)
        bot.reply_to(a, "◍ تم مسح الثانويين بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد ثانويين ليتم مسحهم")

# بدء تشغيل البوت
bot.polling(none_stop=True)