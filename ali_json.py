from config import *
import json

DEVELOPERS = [232499688]
OWNER_BOT = 232499688

# دوال تحميل وتفريغ الملفات
def load_ali_basic_devs():
    try:
        with open('backend/ali_basic_devs.json', 'r') as file:
            ali_basic_devs = json.load(file)
    except FileNotFoundError:
        ali_basic_devs = {'basic_devs': {}}
    return ali_basic_devs

def dump_ali_basic_devs(ali_basic_devs):
    with open('backend/ali_basic_devs.json', 'w') as file:
        json.dump(ali_basic_devs, file)

def load_ali_devs():
    try:
        with open('backend/ali_devs.json', 'r') as file:
            ali_devs = json.load(file)
    except FileNotFoundError:
        ali_devs = {'devs': {}}
    return ali_devs

def dump_ali_devs(ali_devs):
    with open('backend/ali_devs.json', 'w') as file:
        json.dump(ali_devs, file)

def load_ali_basic_creators():
    try:
        with open('backend/ali_basic_creators.json', 'r') as file:
            ali_basic_creators = json.load(file)
    except FileNotFoundError:
        ali_basic_creators = {'basic_creators': {}}
    return ali_basic_creators

def dump_ali_basic_creators(ali_basic_creators):
    with open('backend/ali_basic_creators.json', 'w') as file:
        json.dump(ali_basic_creators, file)

def load_ali_owners():
    try:
        with open('backend/ali_owners.json', 'r') as file:
            ali_owners = json.load(file)
    except FileNotFoundError:
        ali_owners = {'owners': {}}
    return ali_owners

def dump_ali_owners(ali_owners):
    with open('backend/ali_owners.json', 'w') as file:
        json.dump(ali_owners, file)

def load_ali_creators():
    try:
        with open('backend/ali_creators.json', 'r') as file:
            ali_creators = json.load(file)
    except FileNotFoundError:
        ali_creators = {'creators': {}}
    return ali_creators

def dump_ali_creators(ali_creators):
    with open('backend/ali_creators.json', 'w') as file:
        json.dump(ali_creators, file)

def load_ali_admin():
    try:
        with open('backend/ali_admin.json', 'r') as file:
            ali_admin = json.load(file)
    except FileNotFoundError:
        ali_admin = {'admin': {}}
    return ali_admin

def dump_ali_admin(ali_admin):
    with open('backend/ali_admin.json', 'w') as file:
        json.dump(ali_admin, file)

# دوال للتحقق من الرتب باستخدام المتغير a بدلاً من message
def basic_dev(user_id):
    ali_basic_devs = load_ali_basic_devs()
    return user_id in ali_basic_devs['basic_devs']

def dev(user_id):
    ali_devs = load_ali_devs()
    return user_id in ali_devs['devs']

def is_basic_creator(user_id):
    ali_basic_creators = load_ali_basic_creators()
    return user_id in ali_basic_creators['basic_creators']

def owner(user_id, chat_id):
    ali_owners = load_ali_owners()
    return chat_id in ali_owners['owners'] and user_id in ali_owners['owners'][chat_id]['owner_id']

def creator(user_id, chat_id):
    ali_creators = load_ali_creators()
    return chat_id in ali_creators['creators'] and user_id in ali_creators['creators'][chat_id]['creator_id']

def admin(user_id, chat_id):
    ali_admin = load_ali_admin()
    return chat_id in ali_admin['admin'] and user_id in ali_admin['admin'][chat_id]['admin_id']

# فحص ما إذا كان المستخدم مطورًا أو مالكًا باستخدام المتغير a
def owner_id_ali(user_id):
    return user_id == OWNER_BOT

def programmer_ali(user_id):
    return user_id in DEVELOPERS

# اختبار الوظائف على الرسائل
@bot.message_handler(commands=['check_dev'])
def check_dev(a):
    if dev(a.from_user.id):
        bot.reply_to(a, "أنت مطور!")
    else:
        bot.reply_to(a, "أنت لست مطور.")

@bot.message_handler(commands=['check_owner'])
def check_owner(a):
    if owner(a.from_user.id, str(a.chat.id)):
        bot.reply_to(a, "أنت مالك!")
    else:
        bot.reply_to(a, "أنت لست مالك.")

@bot.message_handler(commands=['check_basic_creator'])
def check_basic_creator(a):
    if is_basic_creator(a.from_user.id):
        bot.reply_to(a, "أنت منشئ أساسي!")
    else:
        bot.reply_to(a, "أنت لست منشئ أساسي.")

@bot.message_handler(commands=['check_admin'])
def check_admin(a):
    if admin(a.from_user.id, str(a.chat.id)):
        bot.reply_to(a, "أنت أدمن!")
    else:
        bot.reply_to(a, "أنت لست أدمن.")

@bot.message_handler(commands=['check_owner_id'])
def check_owner_id(a):
    if owner_id_ali(a.from_user.id):
        bot.reply_to(a, "أنت مالك البوت!")
    else:
        bot.reply_to(a, "أنت لست مالك البوت.")

bot.polling()