import logging
from config import *
from telebot import types

# إعداد نظام تسجيل الأخطاء
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# مسارات الملفات النصية
ALI_ADMINS_FILE = 'backend/ali_admin.txt'
ALI_OWNERS_FILE = 'backend/ali_owners.txt'

# تحميل بيانات الادمنية من ملف نصي
def load_ali_admin():
    try:
        with open(ALI_ADMINS_FILE, 'r') as file:
            lines = file.read().splitlines()  # قراءة كل الأسطر
            admins = {}
            for line in lines:
                line = line.strip()  # إزالة المسافات الزائدة
                if not line:  # تجاهل الأسطر الفارغة
                    continue
                try:
                    chat_id, admin_id = line.split(':')
                    if chat_id not in admins:
                        admins[chat_id] = {'admin_id': []}
                    admins[chat_id]['admin_id'].append(admin_id)
                except ValueError:
                    logging.error(f"خطأ في تنسيق السطر: {line}")
            logging.info(f"تم تحميل بيانات الادمنية بنجاح من {ALI_ADMINS_FILE}")
            return admins
    except FileNotFoundError:
        logging.error(f"خطأ: الملف {ALI_ADMINS_FILE} غير موجود.")
        return {}  # إذا كان الملف غير موجود، نعيد قاموس فارغ
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تحميل الادمنية: {e}")

# تفريغ بيانات الادمنية إلى ملف نصي
def dump_ali_admin(ali_admins):
    try:
        with open(ALI_ADMINS_FILE, 'w') as file:
            for chat_id, admin_data in ali_admins.items():
                for admin_id in admin_data['admin_id']:
                    file.write(f"{chat_id}:{admin_id}\n")  # كتابة كل زوج من معرف المجموعة والادمن
        logging.info(f"تم تفريغ بيانات الادمنية بنجاح إلى {ALI_ADMINS_FILE}")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تفريغ بيانات الادمنية: {e}")

# تحميل بيانات المالكين من ملف نصي
def load_ali_owners():
    try:
        with open(ALI_OWNERS_FILE, 'r') as file:
            lines = file.read().splitlines()  # قراءة كل الأسطر
            owners = {}
            for line in lines:
                line = line.strip()  # إزالة المسافات الزائدة
                if not line:  # تجاهل الأسطر الفارغة
                    continue
                try:
                    chat_id, owner_id = line.split(':')
                    owners[chat_id] = {'owner_id': [owner_id]}
                except ValueError:
                    logging.error(f"خطأ في تنسيق السطر: {line}")
            logging.info(f"تم تحميل بيانات المالكين بنجاح من {ALI_OWNERS_FILE}")
            return owners
    except FileNotFoundError:
        logging.error(f"خطأ: الملف {ALI_OWNERS_FILE} غير موجود.")
        return {}  # إذا كان الملف غير موجود، نعيد قاموس فارغ
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تحميل المالكين: {e}")

# تفريغ بيانات المالكين إلى ملف نصي
def dump_ali_owners(ali_owners):
    try:
        with open(ALI_OWNERS_FILE, 'w') as file:
            for chat_id, owner_data in ali_owners.items():
                owner_id = owner_data['owner_id'][0]
                file.write(f"{chat_id}:{owner_id}\n")  # كتابة كل زوج من معرف المجموعة والمالك
        logging.info(f"تم تفريغ بيانات المالكين بنجاح إلى {ALI_OWNERS_FILE}")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تفريغ بيانات المالكين: {e}")

# دالة التفعيل التي تقوم بإضافة المالك إلى ملف المالكين والمدراء إلى ملف الادمنية
def update_admins_and_owner(a):
    try:
        chat_id = str(a.chat.id)
        Ali = a.from_user
        logging.info(f"Received activation command from chat: {chat_id}, by user: {Ali.id}")

        ali_admins = load_ali_admin()
        ali_owners = load_ali_owners()

        owner_id = None
        ali_owner = None

        # الحصول على قائمة المدراء في المجموعة
        chat_members = bot.get_chat_administrators(chat_id)

        # إضافة المدراء إلى قائمة الأدمنية والعثور على المالك
        for admin in chat_members:
            if admin.status == 'creator':  # المالك
                owner_id = str(admin.user.id)
                ali_owner = admin.user
                if chat_id not in ali_owners:
                    ali_owners[chat_id] = {'owner_id': [owner_id]}
                else:
                    if owner_id not in ali_owners[chat_id]['owner_id']:
                        ali_owners[chat_id]['owner_id'].append(owner_id)
                logging.info(f"تم إضافة المالك: {ali_owner.first_name} (ID: {owner_id}) إلى المجموعة {chat_id}")
            elif admin.status == 'administrator':  # المدراء
                admin_id = str(admin.user.id)
                if chat_id not in ali_admins:
                    ali_admins[chat_id] = {'admin_id': []}  # استخدم قائمة فارغة لبدء الإدخال
                if admin_id not in ali_admins[chat_id]['admin_id']:  # تأكد من عدم وجود الإدخال بالفعل
                    ali_admins[chat_id]['admin_id'].append(admin_id)  # أضف الإدمن
                logging.info(f"تم إضافة الادمن: {admin.user.first_name} (ID: {admin_id}) إلى المجموعة {chat_id}")

        # حفظ التغييرات في الملفات النصية
        dump_ali_admin(ali_admins)
        dump_ali_owners(ali_owners)

        # إرسال رسالة تأكيد
        if owner_id:
            bot.send_message(chat_id, f"""◍ تم تفعيل الجروب بواسطة [{Ali.first_name}](tg://user?id={Ali.id})\n\n◍ وتم رفع [{ali_owner.first_name}](tg://user?id={ali_owner.id}) مالك للمجموعة\n◍ وتم إضافة جميع المدراء إلى قائمة الادمنية\n√""", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "لا يوجد مالك في الدردشة.")
            logging.warning(f"لا يوجد مالك للمجموعة {chat_id}.")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تحديث المالكين والمدراء: {e}")