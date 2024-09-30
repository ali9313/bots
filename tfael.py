# دالة التفعيل التي تقوم بإضافة المالك إلى ملف المالكين والمدراء إلى ملف الادمنية
def update_admins_and_owner(a):
    try:
        chat_id = str(a.chat.id)
        Ali = a.from_user
        logging.info(f"Received activation command from chat: {chat_id}, by user: {Ali.id}")

        ali_admins = load_ali_admin()  # تحميل بيانات الأدمنية الحالية
        ali_owners = load_ali_owners()  # تحميل بيانات المالكين الحالية

        owner_id = None
        ali_owner = None

        # الحصول على قائمة المشرفين في المجموعة
        chat_members = bot.get_chat_administrators(chat_id)
        logging.info(f"عدد المشرفين في المجموعة {chat_id}: {len(chat_members)}")

        # إضافة جميع المشرفين إلى قائمة الأدمنية والعثور على المالك
        for admin in chat_members:
            admin_id = str(admin.user.id)
            logging.info(f"فحص: {admin.user.first_name} (ID: {admin_id}), الحالة: {admin.status}")

            if admin.status == 'creator':  # المالك
                owner_id = admin_id
                ali_owner = admin.user
                if chat_id not in ali_owners:
                    ali_owners[chat_id] = {'owner_id': [owner_id]}  # إضافة المالك الجديد
                logging.info(f"تم إضافة المالك: {ali_owner.first_name} (ID: {owner_id}) إلى المجموعة {chat_id}")
            elif admin.status in ['administrator', 'creator']:  # المدراء والمشرفين
                if chat_id not in ali_admins:
                    ali_admins[chat_id] = {'admin_id': []}  # إنشاء قائمة فارغة إذا لم تكن موجودة
                ali_admins[chat_id]['admin_id'].append(admin_id)  # إضافة المشرف
                logging.info(f"تم إضافة المشرف: {admin.user.first_name} (ID: {admin_id}) إلى المجموعة {chat_id}")

        # حفظ التغييرات في الملفات النصية
        dump_ali_admin(ali_admins)
        dump_ali_owners(ali_owners)

        # إرسال رسالة تأكيد
        if owner_id:
            bot.send_message(chat_id, f"""◍ تم تفعيل الجروب بواسطة [{Ali.first_name}](tg://user?id={Ali.id})\n\n◍ وتم رفع [{ali_owner.first_name}](tg://user?id={ali_owner.id}) مالك للمجموعة\n◍ وتم إضافة جميع المشرفين إلى قائمة الادمنية\n√""", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "لا يوجد مالك في الدردشة.")
            logging.warning(f"لا يوجد مالك للمجموعة {chat_id}.")
    except Exception as e:
        logging.error(f"حدث خطأ أثناء تحديث المالكين والمدراء: {e}")