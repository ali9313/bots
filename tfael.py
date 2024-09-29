from config import *
from telebot import types

# مسار ملف المالكين النصي
ALI_OWNERS_FILE = 'backend/ali_owners.txt'

# تحميل بيانات المالكين من ملف نصي
def load_ali_owners():
    try:
        with open(ALI_OWNERS_FILE, 'r') as file:
            lines = file.read().splitlines()  # قراءة كل الأسطر
            owners = {}
            for line in lines:
                chat_id, owner_id = line.split(':')
                owners[chat_id] = {'owner_id': [owner_id]}
            return owners
    except FileNotFoundError:
        return {}  # إذا كان الملف غير موجود، نعيد قاموس فارغ

# تفريغ بيانات المالكين إلى ملف نصي
def dump_ali_owners(ali_owners):
    with open(ALI_OWNERS_FILE, 'w') as file:
        for chat_id, owner_data in ali_owners.items():
            owner_id = owner_data['owner_id'][0]
            file.write(f"{chat_id}:{owner_id}\n")  # كتابة كل زوج من معرف المجموعة والمالك

@bot.message_handler(commands=['تفعيل'])
def update_owners(a):
    chat_id = str(a.chat.id)
    Ali = a.from_user
    ali_owners = load_ali_owners()
    owner_id = None

    # الحصول على قائمة المدراء في المجموعة
    chat_members = bot.get_chat_administrators(chat_id)

    # العثور على المالك
    for admin in chat_members:
        if admin.status == 'creator':  # المالك هو الذي يكون حالته 'creator'
            owner_id = str(admin.user.id)
            ali_owner = admin.user
            break
    
    if owner_id is not None:
        if chat_id not in ali_owners:
            ali_owners[chat_id] = {'owner_id': [owner_id]}
        else:
            existing_owners = ali_owners[chat_id]['owner_id']
            if owner_id not in existing_owners:
                ali_owners[chat_id]['owner_id'].append(owner_id)

        dump_ali_owners(ali_owners)
        bot.send_message(chat_id, f"""◍ تم تفعيل الجروب بواسطة [{Ali.first_name}](tg://user?id={Ali.id})\n\n◍ وتم رفع [{ali_owner.first_name}](tg://user?id={ali_owner.id}) مالك للمجموعة\n√""", parse_mode='Markdown')
    else:
        bot.send_message(chat_id, "لا يوجد مالك في الدردشة.")