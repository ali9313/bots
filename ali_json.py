from config import *

DEVELOPERS = [232499688]
OWNER_BOT = 232499688

# دوال تحميل وتفريغ الملفات النصية
def load_ali_basic_devs():
    ali_basic_devs = {}
    try:
        with open('backend/ali_basic_devs.txt', 'r') as file:
            for line in file:
                dev_id = line.strip()
                ali_basic_devs[dev_id] = True
    except FileNotFoundError:
        print("الملف 'ali_basic_devs.txt' غير موجود.")
    return ali_basic_devs

def dump_ali_basic_devs(ali_basic_devs):
    try:
        with open('backend/ali_basic_devs.txt', 'w') as file:
            for dev_id in ali_basic_devs:
                file.write(f"{dev_id}\n")
    except Exception as e:
        print(f"حدث خطأ أثناء تفريغ 'ali_basic_devs.txt': {e}")

def load_ali_devs():
    ali_devs = {}
    try:
        with open('backend/ali_devs.txt', 'r') as file:
            for line in file:
                dev_id = line.strip()
                ali_devs[dev_id] = True
    except FileNotFoundError:
        print("الملف 'ali_devs.txt' غير موجود.")
    return ali_devs

def dump_ali_devs(ali_devs):
    try:
        with open('backend/ali_devs.txt', 'w') as file:
            for dev_id in ali_devs:
                file.write(f"{dev_id}\n")
    except Exception as e:
        print(f"حدث خطأ أثناء تفريغ 'ali_devs.txt': {e}")

def load_ali_basic_creators():
    ali_basic_creators = {}
    try:
        with open('backend/ali_basic_creators.txt', 'r') as file:
            for line in file:
                creator_id = line.strip()
                ali_basic_creators[creator_id] = True
    except FileNotFoundError:
        print("الملف 'ali_basic_creators.txt' غير موجود.")
    return ali_basic_creators

def dump_ali_basic_creators(ali_basic_creators):
    try:
        with open('backend/ali_basic_creators.txt', 'w') as file:
            for creator_id in ali_basic_creators:
                file.write(f"{creator_id}\n")
    except Exception as e:
        print(f"حدث خطأ أثناء تفريغ 'ali_basic_creators.txt': {e}")

def load_ali_owners():
    ali_owners = {}
    try:
        with open('backend/ali_owners.txt', 'r') as file:
            for line in file:
                chat_id, owner_id = line.strip().split(':')
                if chat_id not in ali_owners:
                    ali_owners[chat_id] = {'owner_id': []}
                ali_owners[chat_id]['owner_id'].append(owner_id)
    except FileNotFoundError:
        print("الملف 'ali_owners.txt' غير موجود.")
    return ali_owners

def dump_ali_owners(ali_owners):
    try:
        with open('backend/ali_owners.txt', 'w') as file:
            for chat_id, data in ali_owners.items():
                for owner_id in data['owner_id']:
                    file.write(f"{chat_id}:{owner_id}\n")
    except Exception as e:
        print(f"حدث خطأ أثناء تفريغ 'ali_owners.txt': {e}")

def load_ali_creators():
    ali_creators = {}
    try:
        with open('backend/ali_creators.txt', 'r') as file:
            for line in file:
                chat_id, creator_id = line.strip().split(':')
                if chat_id not in ali_creators:
                    ali_creators[chat_id] = {'creator_id': []}
                ali_creators[chat_id]['creator_id'].append(creator_id)
    except FileNotFoundError:
        print("الملف 'ali_creators.txt' غير موجود.")
    return ali_creators

def dump_ali_creators(ali_creators):
    try:
        with open('backend/ali_creators.txt', 'w') as file:
            for chat_id, data in ali_creators.items():
                for creator_id in data['creator_id']:
                    file.write(f"{chat_id}:{creator_id}\n")
    except Exception as e:
        print(f"حدث خطأ أثناء تفريغ 'ali_creators.txt': {e}")

def load_ali_admin():
    ali_admin = {}
    try:
        with open('backend/ali_admin.txt', 'r') as file:
            for line in file:
                chat_id, admin_id = line.strip().split(':')
                if chat_id not in ali_admin:
                    ali_admin[chat_id] = {'admin_id': []}
                ali_admin[chat_id]['admin_id'].append(admin_id)
    except FileNotFoundError:
        print("الملف 'ali_admin.txt' غير موجود.")
    return ali_admin

def dump_ali_admin(ali_admin):
    try:
        with open('backend/ali_admin.txt', 'w') as file:
            for chat_id, data in ali_admin.items():
                for admin_id in data['admin_id']:
                    file.write(f"{chat_id}:{admin_id}\n")
    except Exception as e:
        print(f"حدث خطأ أثناء تفريغ 'ali_admin.txt': {e}")

# دوال للتحقق من الرتب باستخدام المتغير a بدلاً من message
def basic_dev(user_id):
    ali_basic_devs = load_ali_basic_devs()
    return str(user_id) in ali_basic_devs

def dev(user_id):
    ali_devs = load_ali_devs()
    return str(user_id) in ali_devs

def is_basic_creator(user_id):
    ali_basic_creators = load_ali_basic_creators()
    return str(user_id) in ali_basic_creators

def owner(user_id, chat_id):
    ali_owners = load_ali_owners()
    return chat_id in ali_owners and str(user_id) in ali_owners[chat_id]['owner_id']

def creator(user_id, chat_id):
    ali_creators = load_ali_creators()
    return chat_id in ali_creators and str(user_id) in ali_creators[chat_id]['creator_id']

def admin(user_id, chat_id):
    ali_admin = load_ali_admin()
    return chat_id in ali_admin and str(user_id) in ali_admin[chat_id]['admin_id']

# فحص ما إذا كان المستخدم مطورًا أو مالكًا باستخدام المتغير a
def owner_id_ali(user_id):
    return user_id == OWNER_BOT

def programmer_ali(user_id):
    return user_id in DEVELOPERS
def check_dev(a):
    print(f"Received command /check_dev from user: {a.from_user.id}")
    if dev(a.from_user.id):
        bot.reply_to(a, "أنت مطور!")
    else:
        bot.reply_to(a, "أنت لست مطور.")
        
def check_owner(a):
    print(f"Received command /check_owner from user: {a.from_user.id}, chat: {a.chat.id}")
    if owner(a.from_user.id, str(a.chat.id)):
        bot.reply_to(a, "أنت مالك!")
    else:
        bot.reply_to(a, "أنت لست مالك.")

def check_basic_creator(a):
    print(f"Received command /check_basic_creator from user: {a.from_user.id}")
    if is_basic_creator(a.from_user.id):
        bot.reply_to(a, "أنت منشئ أساسي!")
    else:
        bot.reply_to(a, "أنت لست منشئ أساسي.")

def check_admin(a):
    print(f"Received command /check_admin from user: {a.from_user.id}, chat: {a.chat.id}")
    if admin(a.from_user.id, str(a.chat.id)):
        bot.reply_to(a, "أنت أدمن!")
    else:
        bot.reply_to(a, "أنت لست أدمن.")

def check_owner_id(a):
    print(f"Received command /check_owner_id from user: {a.from_user.id}")
    if owner_id_ali(a.from_user.id):
        bot.reply_to(a, "أنت مالك البوت!")
    else:
        bot.reply_to(a, "أنت لست مالك البوت.")