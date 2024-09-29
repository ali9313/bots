import logging
from config import *
from ali_json import is_basic_creator, owner, dev, basic_dev, programmer_ali  # إضافة دوال التحقق هنا

# إعداد سجل الأخطاء
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_ali_admin():
    try:
        with open('backend/ali_admin.txt', 'r') as file:
            lines = file.readlines()
            admin_data = {'admin': {}}
            for line in lines:
                line = line.strip()
                if not line:  # تجاهل السطور الفارغة
                    continue
                parts = line.split(':')
                if len(parts) != 2:  # التأكد من أن السطر يحتوي على جزئين
                    logging.warning(f"تنسيق غير صحيح في السطر: {line}")
                    continue
                chat_id, admins = parts
                admin_data['admin'][chat_id] = {'admin_id': admins.split(',') if admins else []}
            logging.info("تم تحميل بيانات الأدمن بنجاح.")
            return admin_data
    except FileNotFoundError:
        logging.error("الملف 'ali_admin.txt' غير موجود.")
        return {'admin': {}}
    except Exception as e:
        logging.error(f"حدث خطأ غير متوقع أثناء تحميل البيانات: {e}")
        return {'admin': {}}

def dump_ali_admin(ali_admin):
    try:
        with open('backend/ali_admin.txt', 'w') as file:
            for chat_id, data in ali_admin['admin'].items():
                admin_ids = ','.join(data['admin_id'])
                file.write(f"{chat_id}:{admin_ids}\n")
        logging.info("تم تفريغ بيانات الأدمن بنجاح.")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تفريغ البيانات إلى 'ali_admin.txt': {e}")

def is_authorized_user(user_id, a):
    chat_id = str(a.chat.id)
    authorized = (
        owner(user_id, chat_id) or
        is_basic_creator(user_id) or
        dev(user_id) or
        basic_dev(user_id) or
        programmer_ali(user_id)  # إضافة التحقق من مطور السورس هنا
    )
    logging.info(f"التحقق من الصلاحيات للمستخدم {user_id}: {'مؤهل' if authorized else 'غير مؤهل'}")
    return authorized

def promote_admin(a):
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
    ali_admin = load_ali_admin()

    # التأكد من أن المستخدم لديه صلاحيات كافية
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب أن تكون منشئ على الأقل لكي تستطيع رفع أدمن.\n√")
        return

    # إضافة المستخدم كأدمن إذا لم يكن موجوداً
    if chat_id not in ali_admin['admin']:
        ali_admin['admin'][chat_id] = {'admin_id': []}

    if user_id in ali_admin['admin'][chat_id]['admin_id']:
        bot.reply_to(a, "◍ هذا المستخدم أدمن بالفعل.\n√")
    else:
        # إضافة المستخدم كأدمن في البيانات
        ali_admin['admin'][chat_id]['admin_id'].append(user_id)
        dump_ali_admin(ali_admin)

        # رفع المستخدم كأدمن فعليًا
        try:
            bot.promote_chat_member(chat_id, user_id,
                can_change_info=True,
                can_post_messages=True,
                can_edit_messages=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True
            )
            user_info = bot.get_chat(user_id)
            user_name = user_info.first_name
            bot.reply_to(a, f"◍ تم رفع  {user_name} كأدمن بنجاح.\n")
            logging.info(f"المستخدم {user_id} تم رفعه كأدمن في المحادثة {chat_id}.")
        except Exception as e:
            logging.error(f"حدث خطأ أثناء رفع المستخدم {user_id} كأدمن: {e}")
            bot.reply_to(a, "◍ حدث خطأ أثناء رفع المستخدم كأدمن.\n√")

def demote_admin(a):
    ali_admin = load_ali_admin()  # تحميل بيانات الأدمن
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
        bot.reply_to(a, "◍ يجب أن تكون منشئ على الأقل لكي تستطيع تنزيل أدمن.\n√")
        return

    if chat_id not in ali_admin['admin']:
        bot.reply_to(a, "لا يوجد مشرفين حتى الأن.")
        return

    if user_id not in ali_admin['admin'][chat_id]['admin_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس أدمن لتنزيله.\n√")
    else:
        ali_admin['admin'][chat_id]['admin_id'].remove(user_id)
        dump_ali_admin(ali_admin)

        # تنزيل المستخدم كأدمن فعليًا
        try:
            bot.promote_chat_member(chat_id, user_id,
                can_change_info=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False
            )
            user_info = bot.get_chat(user_id)
            user_name = user_info.first_name
            bot.reply_to(a, f"◍ تم تنزيل  [{user_name}](tg://user?id={user_id}) من الأدمن بنجاح.\n")
            logging.info(f"المستخدم {user_id} تم تنزيله من الأدمن في المحادثة {chat_id}.")
        except Exception as e:
            logging.error(f"حدث خطأ أثناء تنزيل المستخدم {user_id} من الأدمن: {e}")
            bot.reply_to(a, "◍ حدث خطأ أثناء تنزيل المستخدم.\n√")

def clear_admins(a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    # التأكد من أن المستخدم لديه صلاحيات كافية
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب أن تكون منشئ على الأقل لاستخدام الأمر.\n√")
        return

    if chat_id in ali_admin['admin']:
        # مسح جميع الأدمنيه
        admin_ids = ali_admin['admin'][chat_id]['admin_id']  # احفظ قائمة الأدمنية الحالية
        ali_admin['admin'][chat_id]['admin_id'] = []
        dump_ali_admin(ali_admin)
        
        # إزالة صلاحيات الأدمنيه من المجموعة
        for admin_id in admin_ids:
            try:
                bot.promote_chat_member(chat_id, admin_id,
                    can_change_info=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False
                )
            except Exception as e:
                logging.error(f"خطأ أثناء تنزيل المستخدم {admin_id} من الأدمن: {e}")

        bot.reply_to(a, "◍ تم مسح الأدمنيه بنجاح.\n√")
        logging.info(f"تم مسح جميع الأدمنيه في المحادثة {chat_id}.")
    else:
        bot.reply_to(a, "لا يوجد أدمنيه ليتم مسحهم.")

def get_admins(a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if chat_id not in ali_admin['admin']:
        bot.reply_to(a, "لا يوجد مشرفين في هذه الدردشة.")
        return

    admins = ali_admin['admin'][chat_id]['admin_id']
    if not admins:
        bot.reply_to(a, "لا يوجد مشرفين في هذه الدردشة.")
    else:
        admin_names = []
        for admin_id in admins:
            try:
                user = bot.get_chat(admin_id)
                admin_names.append(f"[{user.first_name}](tg://user?id={user.id})")
            except Exception as e:
                logging.error(f"خطأ في استدعاء معلومات المشرف: {e}")
                continue

        if admin_names:
            admin_list = "\n".join(admin_names)
            bot.reply_to(a, f"◍ قائمة المشرفين:\n\n{admin_list}", parse_mode='Markdown')
            logging.info(f"تم عرض قائمة المشرفين في المحادثة {chat_id}.")
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المشرفين.")