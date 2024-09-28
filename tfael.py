from config import *
import json
from telebot import types

# تحميل وتفريغ بيانات المالكين والمديرين
def load_ali_owners():
    try:
        with open('backend/ali_owners.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'owners': {}}

def dump_ali_owners(ali_owners):
    with open('backend/ali_owners.json', 'w') as file:
        json.dump(ali_owners, file)

def load_ali_admin():
    try:
        with open('backend/ali_admin.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'admin': {}}

def dump_ali_admin(ali_admin):
    with open('backend/ali_admin.json', 'w') as file:
        json.dump(ali_admin, file)

@bot.message_handler(commands=['تفعيل'])
def update_owners(a):
    chat_id = str(a.chat.id)
    Ali = a.from_user
    ali_owners = load_ali_owners()
    ali_admin = load_ali_admin()
    owner_id = None
    
    # الحصول على قائمة المدراء في المجموعة
    chat_members = bot.get_chat_administrators(chat_id)
    admins_id = [str(admin.user.id) for admin in chat_members if not admin.user.is_bot]

    if chat_id not in ali_admin['admin']:
        ali_admin['admin'][chat_id] = {'admin_id': admins_id}
        new_admins = admins_id  # جميع الأدمين الجدد
    else:
        existing_admins = ali_admin['admin'][chat_id]['admin_id']
        new_admins = [admin_id for admin_id in admins_id if admin_id not in existing_admins]
        ali_admin['admin'][chat_id]['admin_id'].extend(new_admins)

    dump_ali_admin(ali_admin)
    count = len(new_admins)

    bot.send_message(chat_id, f"""◍ تم تفعيل الجروب بواسطة [{Ali.first_name}](tg://user?id={Ali.id})\n\n◍ وتمت اضافة {count} مستخدمين الى الادمن\n√""", parse_mode='Markdown')

    # العثور على المالك
    for admin in chat_members:
        if admin.status == 'creator':
            owner_id = str(admin.user.id)
            ali_owner = admin.user
            break
    
    if owner_id is not None:
        if chat_id not in ali_owners['owners']:
            ali_owners['owners'][chat_id] = {'owner_id': [owner_id]}
        else:
            existing_owners = ali_owners['owners'][chat_id]['owner_id']
            if owner_id not in existing_owners:
                ali_owners['owners'][chat_id]['owner_id'].append(owner_id)

        dump_ali_owners(ali_owners)
        bot.send_message(chat_id, f"""◍ تم تفعيل الجروب بواسطة [{Ali.first_name}](tg://user?id={Ali.id})\n\n◍ وتم رفع [{ali_owner.first_name}](tg://user?id={ali_owner.id}) مالك للمجموعة\n√""", parse_mode='Markdown')
    else:
        bot.send_message(chat_id, "لا يوجد مالك في الدردشة.")

