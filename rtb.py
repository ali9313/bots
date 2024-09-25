from config import bot
from collections import defaultdict
import os

# تعريف الرتب
roles = {
    'مواطن': 1,
    'موظف حكومي': 2,
    'رئيس الجمهورية': 3
}
MAHIIB_ID = 232499688  # معرف رئيس الجمهورية

# اسم الملف الذي سيتم تخزين الرتب فيه
roles_file = "backend/user_roles.txt"

# قائمة الأعضاء مع رتبهم (تحتوي على قائمة من الرتب)
members = defaultdict(lambda: ['مواطن'])  # افتراضي: قائمة تحتوي على "مواطن"

# دالة لتحميل الرتب من الملف
def load_roles():
    if os.path.exists(roles_file):
        with open(roles_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:  # تحقق مما إذا كان الملف غير فارغ
                for line in lines:
                    line = line.strip()
                    if not line:  # تجاهل السطر الفارغ
                        continue
                    try:
                        member_id, role_name = line.split(',', 1)
                        if role_name in roles:  # إضافة الرتبة فقط إذا كانت معرفة
                            members[member_id].append(role_name)
                            print(f"تم إضافة الرتبة '{role_name}' للعضو {member_id}.")  # رسالة تصحيح
                    except ValueError:
                        print(f"خطأ في قراءة السطر: {line}")  # تسجيل الخطأ في قراءة السطر
            else:
                print("الملف فارغ، سيتم تعيين رتبة افتراضية 'مواطن' لجميع المستخدمين.")

    # تعيين رتبة رئيس الجمهورية عند بداية تشغيل البوت
    if str(MAHIIB_ID) not in members:
        members[str(MAHIIB_ID)] = ['رئيس الجمهورية']
        print("تم تعيين رتبة رئيس الجمهورية.")  # رسالة تصحيح

# دالة لحفظ الرتب إلى الملف
def save_roles():
    with open(roles_file, 'w', encoding='utf-8') as file:
        for member_id, role_list in members.items():
            for role_name in role_list:
                file.write(f"{member_id},{role_name}\n")
                print(f"تم حفظ الرتبة '{role_name}' للعضو {member_id}.")  # رسالة تصحيح

# دالة لمنح رتبة لأحد الأعضاء من خلال الرسالة
def promote_user(a):
    member_id = str(a.reply_to_message.from_user.id if a.reply_to_message else a.from_user.id)  # الحصول على معرّف المستخدم

    # استخراج الرتبة من نص الرسالة (إزالة الكلمة الأولى "رفع")
    role_name = ' '.join(a.text.split()[1:])  # أخذ كل الكلمات بعد الكلمة الأولى

    print(f"محاولة منح الرتبة '{role_name}' للعضو {member_id}.")  # رسالة تصحيح

    if role_name == 'رئيس الجمهورية':
        bot.reply_to(a, "رئيس الجمهورية واحد ميصير ثنين")
    elif role_name in roles:  # فقط الرتب المعرفة في القائمة
        current_roles = members[member_id]

        # تحقق مما إذا كانت الرتبة الجديدة أعلى من الرتبة الحالية
        current_rank = max(roles[role] for role in current_roles if role in roles)
        if roles[role_name] > current_rank:
            # إذا كانت الرتبة الجديدة أعلى، قم بإزالة جميع الرتب القديمة
            members[member_id] = [role_name]  # الاحتفاظ فقط بالرتبة الجديدة
            print(f"تم رفع رتبة '{role_name}' للعضو {member_id} بعد إزالة الرتب السابقة.")  # رسالة تصحيح
        else:
            # إذا كانت الرتبة الجديدة ليست أعلى، فلا تقم بأي شيء
            bot.reply_to(a, f"لا يمكن رفع الرتبة '{role_name}' للعضو {a.reply_to_message.from_user.first_name} لأنها ليست أعلى من الرتب الحالية.")
            return

        save_roles()  # حفظ التغييرات

        # تحديد الرد المناسب بناءً على الرتبة الجديدة
        if role_name == 'مواطن':
            bot.reply_to(a, f"هذا اصلا مواطن {a.reply_to_message.from_user.first_name}.")
        elif role_name == 'موظف حكومي':
            bot.reply_to(a, f"حلو صار موظف {a.reply_to_message.from_user.first_name}.")
        else:
            bot.reply_to(a, f"تم منح الرتبة '{role_name}' للعضو {a.reply_to_message.from_user.first_name}.")
    else:
        # إذا كانت الرتبة غير معرفة
        bot.reply_to(a, f"خطأ: الرتبة '{role_name}' غير موجودة في القائمة.")

# دالة لقراءة رتبة مستخدم من خلال الرسالة
def get_user_role(user_id):
    """إرجاع رتبة المستخدم بناءً على معرفه"""
    role = members.get(str(user_id), ['مواطن'])[0]  # إذا لم يكن له رتبة، افتراضي "مواطن"
    print(f"الرتبة المعادة للعضو {user_id} هي '{role}'.")  # رسالة تصحيح
    return role

def get_user_message_count(user_id):
    """إرجاع عدد الرسائل المرسلة من قبل المستخدم بناءً على معرفه"""
    # هنا يمكن إضافة منطق حساب عدد الرسائل. في هذا المثال، سأعيد 0 كمؤشر.
    return 0  # عدل هذا حسب المنطق المطلوب

def send_user_info(a):
    """إرسال معلومات المستخدم"""
    # إذا كان المستخدم يرد على شخص آخر
    if a.reply_to_message:
        user = a.reply_to_message.from_user  # الحصول على معلومات الشخص المُرد عليه
    else:
        user = a.from_user  # الحصول على معلومات الشخص الذي أرسل الأمر

    user_id = user.id  # الحصول على آيدي المستخدم
    user_name = user.first_name
    user_username = user.username if user.username else "معنده"
    user_role = get_user_role(user_id)  # استدعاء دالة لجلب رتبة المستخدم
    user_messages = get_user_message_count(user_id)  # الحصول على عدد رسائل المستخدم

    # التأكد من أن الرتبة موجودة قبل إضافتها إلى الكليشة
    if user_role not in roles:
        user_role = "مواطن"  # تعيين الرتبة الافتراضية

    # إنشاء الكليشة مع الرتبة
    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ ID ⇢ {user_id}
    ‣ USER ⇢ @{user_username}
    ‣ ROLE ⇢ {user_role}  
    ‣ MESSAGES ⇢ {user_messages}
    ⋆─┄─┄─┄─┄─⋆
    """

    # جلب الصورة الشخصية للمستخدم إذا كانت متاحة
    photos = bot.get_user_profile_photos(user.id)

    if photos.total_count > 0:
        bot.send_photo(a.chat.id, photos.photos[0][-1].file_id, caption=message_text)
    else:
        bot.send_message(a.chat.id, message_text)

load_roles()