import logging
from config import *
from ali_json import *

# إعداد سجل الأخطاء
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_ali_distinct():
    try:
        with open('backend/ali_distinct.txt', 'r') as file:
            lines = file.readlines()
            distinct_data = {'distinct': {}}
            for line in lines:
                line = line.strip()
                if not line:  # تجاهل السطور الفارغة
                    continue
                parts = line.split(':')
                if len(parts) != 2:  # التأكد من أن السطر يحتوي على جزئين
                    logging.warning(f"تنسيق غير صحيح في السطر: {line}")
                    continue
                chat_id, distincts = parts
                distinct_data['distinct'][chat_id] = {'distinct_id': distincts.split(',') if distincts else []}
            logging.info("تم تحميل بيانات الـ distinct بنجاح.")
            return distinct_data
    except FileNotFoundError:
        logging.error("الملف 'ali_distinct.txt' غير موجود.")
        return {'distinct': {}}
    except Exception as e:
        logging.error(f"حدث خطأ غير متوقع أثناء تحميل البيانات: {e}")
        return {'distinct': {}}

def dump_ali_distinct(ali_distinct):
    try:
        with open('backend/ali_distinct.txt', 'w') as file:
            for chat_id, data in ali_distinct['distinct'].items():
                distinct_ids = ','.join(data['distinct_id'])
                file.write(f"{chat_id}:{distinct_ids}\n")
        logging.info("تم تفريغ بيانات الـ distinct بنجاح.")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تفريغ البيانات إلى 'ali_distinct.txt': {e}")

def is_authorized_user(user_id, a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()  # تحميل بيانات الأدمن
    ali_distinct = load_ali_distinct()  # تحميل بيانات الـ distinct
    authorized = (
        owner(user_id, chat_id) or
        is_basic_creator(user_id) or
        dev(user_id) or
        basic_dev(user_id) or
        programmer_ali(user_id) or
        (chat_id in ali_admin['admin'] and user_id in ali_admin['admin'][chat_id]['admin_id']) or  # التحقق من كونه أدمن
        (chat_id in ali_distinct['distinct'] and user_id in ali_distinct['distinct'][chat_id]['distinct_id'])  # التحقق من كونه من الـ distinct
    )
    logging.info(f"التحقق من الصلاحيات للمستخدم {user_id}: {'مؤهل' if authorized else 'غير مؤهل'}")
    return authorized

def add_distinct(a):
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif a.reply_to_message is None and len(a.text.split()) > 1:
        target = a.text.split()[1]
        try:
            user = bot.get_chat(target)
            user_id = str(user.id)
        except Exception as e:
            logging.error(f"خطأ في استدعاء المستخدم: {e}")
            bot.reply_to(a, "لا يمكن العثور على المستخدم.")
            return
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم أو إدخال معرفه.")
        return

    chat_id = str(a.chat.id)
    ali_distinct = load_ali_distinct()

    # التأكد من أن المستخدم لديه صلاحيات كافية
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب أن تكون منشئ على الأقل لكي تستطيع إضافة مميز.\n√")
        return

    # إضافة المستخدم كمميز إذا لم يكن موجوداً
    if chat_id not in ali_distinct['distinct']:
        ali_distinct['distinct'][chat_id] = {'distinct_id': []}

    if user_id in ali_distinct['distinct'][chat_id]['distinct_id']:
        bot.reply_to(a, "◍ هذا المستخدم مميز بالفعل.\n√")
    else:
        # إضافة المستخدم كمميز في البيانات
        ali_distinct['distinct'][chat_id]['distinct_id'].append(user_id)
        dump_ali_distinct(ali_distinct)

        bot.reply_to(a, "◍ تم إضافة المميز بنجاح.\n")
        logging.info(f"المستخدم {user_id} تم إضافته كمميز في المحادثة {chat_id}.")

def remove_distinct(a):
    ali_distinct = load_ali_distinct()  # تحميل بيانات الـ distinct
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif a.reply_to_message is None and len(a.text.split()) > 1:
        target = a.text.split()[1]
        try:
            user = bot.get_chat(target)
            user_id = str(user.id)
        except Exception as e:
            logging.error(f"خطأ في استدعاء المستخدم: {e}")
            bot.reply_to(a, "لا يمكن العثور على المستخدم.")
            return
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم أو إدخال معرفه.")
        return

    chat_id = str(a.chat.id)

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب أن تكون منشئ على الأقل لكي تستطيع إزالة مميز.\n√")
        return

    if chat_id not in ali_distinct['distinct']:
        bot.reply_to(a, "لا يوجد مميزون حتى الأن.")
        return

    if user_id not in ali_distinct['distinct'][chat_id]['distinct_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس مميزًا لتنزيله.\n√")
        return

    # إزالة المستخدم من قائمة المميزين في ملف ali_distinct.txt
    ali_distinct['distinct'][chat_id]['distinct_id'].remove(user_id)
    dump_ali_distinct(ali_distinct)

    bot.reply_to(a, "◍ تم إزالة المميز بنجاح.\n")
    logging.info(f"المستخدم {user_id} تم إزالته من المميزين في المحادثة {chat_id}.")

def clear_distinct(a):
    chat_id = str(a.chat.id)
    ali_distinct = load_ali_distinct()

    # التأكد من أن المستخدم لديه صلاحيات كافية
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب أن تكون منشئ على الأقل لاستخدام الأمر.\n√")
        return

    if chat_id in ali_distinct['distinct']:
        # مسح جميع المميزين
        ali_distinct['distinct'][chat_id]['distinct_id'] = []  # احفظ قائمة المميزين الحالية
        dump_ali_distinct(ali_distinct)
        
        bot.reply_to(a, "◍ تم مسح المميزين بنجاح.\n√")
        logging.info(f"تم مسح جميع المميزين في المحادثة {chat_id}.")
    else:
        bot.reply_to(a, "لا يوجد مميزون ليتم مسحهم.")

def get_distinct(a):
    chat_id = str(a.chat.id)
    ali_distinct = load_ali_distinct()

    if chat_id not in ali_distinct['distinct']:
        bot.reply_to(a, "لا يوجد مميزون في هذه الدردشة.")
        return

    distinct = ali_distinct['distinct'][chat_id]['distinct_id']
    if not distinct:
        bot.reply_to(a, "لا يوجد مميزون في هذه الدردشة.")
    else:
        distinct_names = []
        for distinct_id in distinct:
            try:
                user = bot.get_chat(distinct_id)
                distinct_names.append(f"[{user.first_name}](tg://user?id={user.id})")
            except Exception as e:
                logging.error(f"خطأ في استدعاء معلومات المميز: {e}")
                continue

        if distinct_names:
            distinct_list = "\n".join(distinct_names)
            bot.reply_to(a, f"◍ قائمة المميزين:\n\n{distinct_list}", parse_mode='Markdown')
            logging.info(f"تم عرض قائمة المميزين في المحادثة {chat_id}.")
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المميزين.")