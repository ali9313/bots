import logging
from config import *
from ali_json import *
from telebot import types

# إعداد نظام تسجيل الأخطاء ليتم الطباعة إلى وحدة التحكم أيضًا
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# مسارات الملفات النصية
ALI_ADMINS_FILE = 'backend/ali_admin.txt'
ALI_OWNERS_FILE = 'backend/ali_owners.txt'

# تحميل بيانات الادمنية من ملف نصي
def load_ali_admin():
    try:
        with open(ALI_ADMINS_FILE, 'r') as file:
            lines = file.read().splitlines()
            admins = {}
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    chat_id, admin_id = line.split(',')  # تغيير هنا إلى فاصلة
                    if chat_id not in admins:
                        admins[chat_id] = {'admin_id': []}
                    admins[chat_id]['admin_id'].append(admin_id)
                except ValueError:
                    logging.error(f"خطأ في تنسيق السطر: {line}")
            logging.info(f"تم تحميل بيانات الادمنية بنجاح من {ALI_ADMINS_FILE}")
            return admins
    except FileNotFoundError:
        logging.error(f"خطأ: الملف {ALI_ADMINS_FILE} غير موجود.")
        return {}
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تحميل الادمنية: {e}")
        return {}

# تفريغ بيانات الادمنية إلى ملف نصي
def dump_ali_admin(ali_admins):
    try:
        # فتح الملف في وضع الإضافة 'a' بدلاً من 'w'
        with open(ALI_ADMINS_FILE, 'a') as file:
            for chat_id, admin_data in ali_admins.items():
                for admin_id in admin_data['admin_id']:
                    # كتابة كل إدمن جديد فقط إذا لم يكن قد تمت إضافته سابقاً
                    file.write(f"{chat_id},{admin_id}\n")  # تغيير هنا إلى فاصلة
        logging.info(f"تم تفريغ بيانات الادمنية بنجاح إلى {ALI_ADMINS_FILE}")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تفريغ بيانات الادمنية: {e}")

# تحميل بيانات المالكين من ملف نصي
def load_ali_owners():
    try:
        with open(ALI_OWNERS_FILE, 'r') as file:
            lines = file.read().splitlines()
            owners = {}
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    chat_id, owner_id = line.split(',')  # تغيير هنا إلى فاصلة
                    if chat_id not in owners:
                        owners[chat_id] = {'owner_id': []}
                    owners[chat_id]['owner_id'].append(owner_id)
                except ValueError:
                    logging.error(f"خطأ في تنسيق السطر: {line}")
            logging.info(f"تم تحميل بيانات المالكين بنجاح من {ALI_OWNERS_FILE}")
            return owners
    except FileNotFoundError:
        logging.error(f"خطأ: الملف {ALI_OWNERS_FILE} غير موجود.")
        return {}
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تحميل بيانات المالكين: {e}")
        return {}

# تفريغ بيانات المالكين إلى ملف نصي
def dump_ali_owners(ali_owners):
    try:
        with open(ALI_OWNERS_FILE, 'a') as file:
            for chat_id, owner_data in ali_owners.items():
                for owner_id in owner_data['owner_id']:
                    file.write(f"{chat_id},{owner_id}\n")  # تغيير هنا إلى فاصلة
        logging.info(f"تم تفريغ بيانات المالكين بنجاح إلى {ALI_OWNERS_FILE}")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تفريغ بيانات المالكين: {e}")

# دالة التفعيل التي تقوم بإضافة المالك إلى ملف المالكين والمدراء إلى ملف الادمنية
def update_admins_and_owner(a):
    try:
        chat_id = str(a.chat.id)
        Ali = a.from_user
        logging.info(f"Received activation command from chat: {chat_id}, by user: {Ali.id}")
        
        # إضافة تتبع لمخرجات الطباعة لزيادة وضوح الخطأ
        print(f"Received activation command from chat: {chat_id}, by user: {Ali.id}")

        ali_admins = load_ali_admin()
        ali_owners = load_ali_owners()

        owner_id = None
        ali_owner = None

        # الحصول على قائمة المشرفين في المجموعة
        try:
            chat_members = bot.get_chat_administrators(chat_id)
        except Exception as e:
            logging.error(f"خطأ في الحصول على المشرفين: {e}")
            print(f"خطأ في الحصول على المشرفين: {e}")
            return

        logging.info(f"عدد المشرفين في المجموعة {chat_id}: {len(chat_members)}")
        print(f"عدد المشرفين في المجموعة {chat_id}: {len(chat_members)}")

        # إضافة جميع المشرفين إلى قائمة الأدمنية والعثور على المالك
        for admin in chat_members:
            admin_id = str(admin.user.id)
            logging.info(f"فحص: {admin.user.first_name} (ID: {admin_id}), الحالة: {admin.status}")
            print(f"فحص: {admin.user.first_name} (ID: {admin_id}), الحالة: {admin.status}")

            if admin.status == 'creator':  # المالك
                owner_id = admin_id
                ali_owner = admin.user
                if chat_id not in ali_owners:
                    ali_owners[chat_id] = {'owner_id': [owner_id]}
                logging.info(f"تم إضافة المالك: {ali_owner.first_name} (ID: {owner_id}) إلى المجموعة {chat_id}")
                print(f"تم إضافة المالك: {ali_owner.first_name} (ID: {owner_id}) إلى المجموعة {chat_id}")
            elif admin.status in ['administrator', 'creator']:  # المدراء والمشرفين
                if chat_id not in ali_admins:
                    ali_admins[chat_id] = {'admin_id': []}
                if admin_id not in ali_admins[chat_id]['admin_id']:  # تجنب التكرار
                    ali_admins[chat_id]['admin_id'].append(admin_id)
                    logging.info(f"تم إضافة المشرف: {admin.user.first_name} (ID: {admin_id}) إلى المجموعة {chat_id}")
                    print(f"تم إضافة المشرف: {admin.user.first_name} (ID: {admin_id}) إلى المجموعة {chat_id}")

        # حفظ التغييرات في الملفات النصية
        dump_ali_admin(ali_admins)
        dump_ali_owners(ali_owners)

        # إرسال رسالة تأكيد
        if owner_id:
            bot.send_message(chat_id, f"""◍ تم تفعيل الجروب بواسطة [{Ali.first_name}](tg://user?id={Ali.id})\n\n◍ وتم رفع [{ali_owner.first_name}](tg://user?id={ali_owner.id}) مالك للمجموعة\n◍ وتم إضافة جميع المشرفين إلى قائمة الادمنية\n√""", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "لا يوجد مالك في الدردشة.")
            logging.warning(f"لا يوجد مالك للمجموعة {chat_id}.")
            print(f"لا يوجد مالك للمجموعة {chat_id}.")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تحديث المالكين والمدراء: {e}")
        print(f"حدث خطأ أثناء تحديث المالكين والمدراء: {e}")