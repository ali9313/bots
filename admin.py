from config import *
def load_ali_admin():
    try:
        with open('backend/ali_admin.txt', 'r') as file:
            lines = file.readlines()
            admin_data = {'admin': {}}
            for line in lines:
                chat_id, admins = line.strip().split(':')
                admin_data['admin'][chat_id] = {'admin_id': admins.split(',') if admins else []}
            return admin_data
    except FileNotFoundError:
        print("الملف 'ali_admin.txt' غير موجود.")
        return {'admin': {}}
    except Exception as e:
        print(f"حدث خطأ غير متوقع أثناء تحميل البيانات: {e}")
        return {'admin': {}}

def dump_ali_admin(ali_admin):
    try:
        with open('backend/ali_admin.txt', 'w') as file:
            for chat_id, data in ali_admin['admin'].items():
                admin_ids = ','.join(data['admin_id'])
                file.write(f"{chat_id}:{admin_ids}\n")
    except Exception as e:
        print(f"حدث خطأ أثناء تفريغ البيانات إلى 'ali_admin.txt': {e}")

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
            print(f"خطأ في استدعاء المستخدم: {e}")
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم أو إدخال معرفه.")
        return

    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    # تحقق من الصلاحيات (ضع دوال التحقق الخاصة بك هنا)
    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب ان تكون منشئ على الاقل لكى تستطيع رفع ادمن\n√")
        return

    if chat_id not in ali_admin['admin']:
        ali_admin['admin'][chat_id] = {'admin_id': []}

    if user_id in ali_admin['admin'][chat_id]['admin_id']:
        bot.reply_to(a, "◍ هذا المستخدم ادمن بالفعل\n√")
    else:
        ali_admin['admin'][chat_id]['admin_id'].append(user_id)
        dump_ali_admin(ali_admin)
        bot.reply_to(a, "◍ تم رفع المستخدم ليصبح ادمن\n√")

def demote_admin(a):
    if a.reply_to_message and a.reply_to_message.from_user:
        target = a.reply_to_message.from_user.id
        user_id = str(target)
    elif a.reply_to_message is None and len(a.text.split()) > 1:
        target = a.text.split()[1]
        try:
            user = bot.get_chat(target)
            user_id = str(user.id)
        except Exception as e:
            print(f"خطأ في استدعاء المستخدم: {e}")
            bot.reply_to(a, "لا يمكن العثور على المستخدم")
            return
    else:
        bot.reply_to(a, "يرجى الرد على رسالة المستخدم أو إدخال معرفه.")
        return

    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب ان تكون منشئ على الاقل لكى تستطيع تنزيل ادمن\n√")
        return

    if chat_id not in ali_admin['admin']:
        bot.reply_to(a, "لا يوجد مشرفين حتى الأن")
        return

    if user_id not in ali_admin['admin'][chat_id]['admin_id']:
        bot.reply_to(a, "◍ هذا المستخدم ليس ادمن لتنزيله\n√")
    else:
        ali_admin['admin'][chat_id]['admin_id'].remove(user_id)
        dump_ali_admin(ali_admin)
        bot.reply_to(a, "◍ تم تنزيل المستخدم من الادمن بنجاح\n√")


def clear_admins(a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if not is_authorized_user(a.from_user.id, a):
        bot.reply_to(a, "◍ يجب ان تكون منشئ على الاقل لاستخدام الامر\n√")
        return

    if chat_id in ali_admin['admin']:
        ali_admin['admin'][chat_id]['admin_id'] = []
        dump_ali_admin(ali_admin)
        bot.reply_to(a, "◍ تم مسح الادمنيه بنجاح\n√")
    else:
        bot.reply_to(a, "لا يوجد ادمنيه ليتم مسحهم")


def get_admins(a):
    chat_id = str(a.chat.id)
    ali_admin = load_ali_admin()

    if chat_id not in ali_admin['admin']:
        bot.reply_to(a, "لا يوجد مشرفين في هذه الدردشة")
        return

    admins = ali_admin['admin'][chat_id]['admin_id']
    if not admins:
        bot.reply_to(a, "لا يوجد مشرفين في هذه الدردشة")
    else:
        admin_names = []
        for admin_id in admins:
            try:
                user = bot.get_chat(admin_id)
                admin_names.append(f"[{user.first_name}](tg://user?id={user.id})")
            except Exception as e:
                print(f"خطأ في استدعاء معلومات المشرف: {e}")
                continue

        if admin_names:
            admin_list = "\n".join(admin_names)
            bot.reply_to(a, f"◍ قائمة المشرفين:\n\n{admin_list}", parse_mode='Markdown')
        else:
            bot.reply_to(a, "تعذر العثور على معلومات المشرفين")