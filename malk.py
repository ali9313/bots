import logging
from config import *
from ali_json import is_basic_creator, owner, dev, basic_dev, programmer_ali, owner_id_ali

# إعداد logging
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# تحميل المالكين من الملف النصي
def load_ali_owners():
    owners_dict = {"owners": {}}
    try:
        with open('backend/ali_owners.txt', 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue  # تخطي الأسطر الفارغة
                parts = line.split(':', 1)  # تقسيم السطر على أول رمز ':'
                if len(parts) != 2:
                    logging.error(f"خطأ في التنسيق بالسطر {line_num} في ali_owners.txt: {line}")
                    continue  # تخطي السطور ذات التنسيق غير الصحيح
                chat_id, owners = parts
                owners_dict['owners'][chat_id] = {'owner_id': owners.split(',') if owners else []}
    except FileNotFoundError:
        logging.error("ملف ali_owners.txt غير موجود. سيتم إنشاء ملف جديد عند إضافة مالكين.")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تحميل المالكين: {e}")
    return owners_dict

# حفظ المالكين في الملف النصي
def dump_ali_owners(data):
    try:
        with open('backend/ali_owners.txt', 'w') as file:
            for chat_id, info in data['owners'].items():
                owners = ','.join(info['owner_id'])
                file.write(f"{chat_id}:{owners}\n")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء حفظ المالكين: {e}")

# استبدال دالة التحقق بالدالة المحفوظة
def is_authorized_user(user_id, a):
    authorized = (
        programmer_ali(user_id) or
        basic_dev(user_id) or owner_id_ali(user_id) or dev(user_id) or is_basic_creator(user_id)
    )
    logging.info(f"التحقق من الصلاحيات للمستخدم {user_id}: {'مؤهل' if authorized else 'غير مؤهل'}")
    return authorized

def promote_owner(a):
    if not is_authorized_user(a.from_user.id, a):  # تحقق من صلاحيات المستخدم
        bot.reply_to(a, "◍ يجب أن تكون مطورًا أساسيًا لكي تستطيع رفع مالك\n√")
        return

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
    if not is_authorized_user(a.from_user.id, a):  # تحقق من صلاحيات المستخدم
        bot.reply_to(a, "◍ يجب أن تكون مطورًا أساسيًا لكي تستطيع تنزيل مالك\n√")
        return

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
    else:
        bot.reply_to(a, "يرجى تحديد مستخدم")
        return

    chat_id = str(a.chat.id)
    ali_owners = load_ali_owners()

    if chat_id not in ali_owners['owners']:
        bot.reply_to(a, "لا يوجد مالكين في هذه الدردشة حتى الآن")
        return

    if user_id not in ali_owners['owners'][chat_id]['owner_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس مالكًا لتنزيله\n√")
    else:
        ali_owners['owners'][chat_id]['owner_id'].remove(user_id)
        dump_ali_owners(ali_owners)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من المالكين بنجاح\n√")

def clear_owner(a):
    if not is_authorized_user(a.from_user.id, a):  # تحقق من صلاحيات المستخدم
        bot.reply_to(a, "◍ يجب أن تكون مطورًا أساسيًا لاستخدام الأمر\n√")
        return

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
        bot.reply_to(a, "لا يوجد مالكين حتى الآن")
        return

    owners = ali_owners['owners'][chat_id]['owner_id']
    if not owners:
        bot.reply_to(a, "لا يوجد مالكين حتى الآن")
    else:
        owner_names = []
        for owner_id in owners:
            try:
                user = bot.get_chat_member(a.chat.id, int(owner_id))
                owner_names.append(f"[{user.user.first_name}](tg://user?id={user.user.id})" if user.user.username else f"{user.user.first_name}")
            except:
                continue

        if owner_names:
            owner_list = "\n".join(owner_names)
            bot.reply_to(a, f"◍ قائمة المالكين:\n\n{owner_list}", parse_mode='Markdown')
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المالكين")