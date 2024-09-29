from config import *
def load_ali_distinct():
    try:
        with open('backend/ali_distinct.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            ali_distinct = {'admin': {}}
            for line in lines:
                chat_id, admin_ids = line.strip().split(':')
                ali_distinct['admin'][chat_id] = {'admin_id': admin_ids.split(',')}
            return ali_distinct
    except FileNotFoundError:
        return {'admin': {}}

def dump_ali_distinct(ali_distinct):
    with open('backend/ali_distinct.txt', 'w', encoding='utf-8') as file:
        for chat_id, data in ali_distinct['admin'].items():
            admin_ids = ','.join(data['admin_id'])
            file.write(f"{chat_id}:{admin_ids}\n")

def ALI(bot, a):
    # تحقق مما إذا كان المستخدم أدمن أو لديه صلاحيات معينة
    return False  # يمكن تعديلها لاحقاً حسب الحاجة


def promote_distinct(a):
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

    if not ALI(bot, a):
        bot.reply_to(a, """◍ يجب ان تكون ادمن على الاقل لكى تستطيع رفع مميز
√""")
        return

    if chat_id not in ali_distinct['admin']:
        ali_distinct['admin'][chat_id] = {'admin_id': []}

    if user_id in ali_distinct['admin'][chat_id]['admin_id']:
        bot.reply_to(a, """◍ هذا المستخدم مميز بالفعل
√""")
    else:
        ali_distinct['admin'][chat_id]['admin_id'].append(user_id)
        dump_ali_distinct(ali_distinct)
        bot.reply_to(a, """◍ تم رفع المستخدم ليصبح مميز
√""")


def demote_distinct(a):
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

    if not ALI(bot, a):
        bot.reply_to(a, """◍ يجب ان تكون ادمن على الاقل لكى تستطيع تنزيل مميز
√""")
        return

    if chat_id not in ali_distinct['admin']:
        bot.reply_to(a, "لا يوجد مميزين حتى الأن")
        return

    if user_id not in ali_distinct['admin'][chat_id]['admin_id']:
        bot.reply_to(a, """◍ هذا المستخدم ليس مميز لتنزيله
√""")
    else:
        ali_distinct['admin'][chat_id]['admin_id'].remove(user_id)
        dump_ali_distinct(ali_distinct)
        bot.reply_to(a, """◍ تم تنزيل المستخدم من المميزين بنجاح
√""")

def clear_distinct(a):
    chat_id = str(a.chat.id)
    ali_distinct = load_ali_distinct()

    if not ALI(bot, a):
        bot.reply_to(a, """◍ يجب ان تكون ادمن على الاقل لكى تستطيع استخدام الأمر
√""")
        return

    if chat_id in ali_distinct['admin']:
        ali_distinct['admin'][chat_id]['admin_id'] = []
        dump_ali_distinct(ali_distinct)
        bot.reply_to(a, """◍ تم مسح المميزين بنجاح
√""")
    else:
        bot.reply_to(a, "لا يوجد مميزين ليتم مسحهم")

def get_distinct(a):
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
            user = bot.get_chat(int(admin_id))
            if user:
                admin_names.append(f"[{user.first_name}](tg://user?id={user.id})")

        if admin_names:
            admin_list = "\n".join(admin_names)
            bot.reply_to(a, f"◍ قائمة المميزين:\n\n{admin_list}", parse_mode='Markdown')
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المميزين")

