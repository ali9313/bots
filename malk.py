from config import *
def load_ali_owners():
    with open('backend/ali_owners.txt', 'r') as file:
        return eval(file.read()) if file.read() else {"owners": {}}

def dump_ali_owners(data):
    with open('backend/ali_owners.txt', 'w') as file:
        file.write(str(data))



def promote_owner(a):
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif len(a.text.split()) > 1:
        target = a.text.split()[1].strip("@")
        user = bot.get_chat_member(a.chat.id, target)
        if user:
            user_id = str(user.user.id)
        else:
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return
    else:
        bot.reply_to(a, "يرجى تحديد مستخدم")
        return

    chat_id = str(a.chat.id)
    ali_owners = load_ali_owners()

    if chat_id not in ali_owners['owners']:
        ali_owners['owners'][chat_id] = {'owner_id': []}

    if user_id in ali_owners['owners'][chat_id]['owner_id']:
        bot.reply_to(a, "◍ هذا المستخدم مالك بالفعل\n√")
    else:
        ali_owners['owners'][chat_id]['owner_id'].append(user_id)
        dump_ali_owners(ali_owners)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح مالك\n√")



def demote_owner(a):
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif len(a.text.split()) > 1:
        target = a.text.split()[1].strip("@")
        user = bot.get_chat_member(a.chat.id, target)
        if user:
            user_id = str(user.user.id)
        else:
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return
    else:
        bot.reply_to(a, "يرجى تحديد مستخدم")
        return

    chat_id = str(a.chat.id)
    ali_owners = load_ali_owners()

    if chat_id not in ali_owners['owners']:
        bot.reply_to(a, "لا يوجد مالكين في هذه الدردشة حتى الأن")
        return

    if user_id not in ali_owners['owners'][chat_id]['owner_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس مالك لتنزيله\n√")
    else:
        ali_owners['owners'][chat_id]['owner_id'].remove(user_id)
        dump_ali_owners(ali_owners)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من المالكين بنجاح\n√")


def clear_owner(a):
    chat_id = str(a.chat.id)
    ali_owners = load_ali_owners()

    if chat_id in ali_owners['owners']:
        ali_owners['owners'][chat_id]['owner_id'] = []
        dump_ali_owners(ali_owners)
        bot.reply_to(a, "◍ تم مسح المالكين بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد مالكين ليتم مسحهم")


def get_owner(a):
    chat_id = str(a.chat.id)
    ali_owners = load_ali_owners()

    if chat_id not in ali_owners['owners']:
        bot.reply_to(a, "لا يوجد مالكين حتى الأن")
        return

    owners = ali_owners['owners'][chat_id]['owner_id']
    if not owners:
        bot.reply_to(a, "لا يوجد مالكين حتى الأن")
    else:
        owner_names = []
        for owner_id in owners:
            user = bot.get_chat_member(a.chat.id, int(owner_id))
            if user:
                owner_names.append(f"[{user.user.first_name}](tg://user?id={user.user.id})")

        if owner_names:
            owner_list = "\n".join(owner_names)
            bot.reply_to(a, f"◍ قائمة المالكين:\n\n{owner_list}")
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المالكين")