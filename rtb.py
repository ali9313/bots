from config import bot
from collections import defaultdict
import os

# تعريف الرتب
roles = {
    'مواطن': 1,
    'موظف حكومي': 2,
    'رئيس الجمهورية': 3
}
MAHIIB_ID = 232499688  
roles_file = "backend/user_roles.txt"
members = defaultdict(lambda: ['مواطن'])  

# دالة لتحميل الرتب
def load_roles():
    if os.path.exists(roles_file):
        with open(roles_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:  
                for line in lines:
                    line = line.strip()
                    if not line:  
                        continue
                    try:
                        member_id, role_name = line.split(',', 1)
                        if role_name in roles:  
                            members[member_id].append(role_name)
                    except ValueError:
                        pass
            else:
                print("الملف فارغ، سيتم تعيين رتبة افتراضية 'مواطن' لجميع المستخدمين.")
    if str(MAHIIB_ID) not in members:
        members[str(MAHIIB_ID)] = ['رئيس الجمهورية']

# دالة لحفظ الرتب
def save_roles():
    with open(roles_file, 'w', encoding='utf-8') as file:
        for member_id, role_list in members.items():
            for role_name in role_list:
                file.write(f"{member_id},{role_name}\n")

# دالة لرفع رتبة المستخدم
def promote_user(a):
    member_id = str(a.reply_to_message.from_user.id if a.reply_to_message else a.from_user.id)  
    role_name = ' '.join(a.text.split()[1:])  
    if role_name == 'رئيس الجمهورية':
        bot.reply_to(a, "رئيس الجمهورية واحد ميصير ثنين")
    elif role_name in roles:  
        current_roles = members[member_id]
        current_rank = max(roles[role] for role in current_roles if role in roles)
        if roles[role_name] > current_rank:
            members[member_id] = [role_name] 
        else:
            bot.reply_to(a, f"لا يمكن رفع الرتبة '{role_name}' للعضو {a.reply_to_message.from_user.first_name} لأنها ليست أعلى من الرتب الحالية.")
            return
        save_roles() 
        if role_name == 'مواطن':
            bot.reply_to(a, f"هذا اصلا مواطن {a.reply_to_message.from_user.first_name}.")
        elif role_name == 'موظف حكومي':
            bot.reply_to(a, f"حلو صار موظف {a.reply_to_message.from_user.first_name}.")
        else:
            bot.reply_to(a, f"تم منح الرتبة '{role_name}' للعضو {a.reply_to_message.from_user.first_name}.")
    else:
        bot.reply_to(a, f"خطأ: الرتبة '{role_name}' غير موجودة في القائمة.")

# دالة لتنزيل رتبة موظف حكومي
def demote_user(a):
    member_id = str(a.reply_to_message.from_user.id)  
    current_roles = members[member_id]
    if 'موظف حكومي' in current_roles:
        members[member_id].remove('موظف حكومي')
        members[member_id].append('مواطن')  
        save_roles()  
        bot.reply_to(a, f"تم تحويل {a.reply_to_message.from_user.first_name} من موظف حكومي إلى مواطن.")
    else:
        bot.reply_to(a, f"العضو {a.reply_to_message.from_user.first_name} ليس لديه رتبة موظف حكومي.")

# دالة للحصول على رتبة المستخدم
def get_user_role(user_id):
    role = members.get(str(user_id), ['مواطن'])[0]  
    return role

# دالة للتحقق من رتبة المستخدم في الكروب
def check_sender_role(a):
    sender_id = a.from_user.id  # الحصول على معرف مرسل الأمر
    sender_role = get_user_role(sender_id)  # الحصول على رتبة المرسل
    
    # التحقق من كونه مشرفاً أو مالكاً للكروب
    chat_member = bot.get_chat_member(a.chat.id, sender_id)  # الحصول على معلومات العضو في الكروب
    
    if chat_member.status in ['administrator', 'creator']:  # إذا كان مشرفاً أو مالكاً
        is_admin = 'مشرف'
    else:
        is_admin = 'عضو'
        
    # إرسال رسالة توضح الرتبة في الكروب والبوت
    bot.reply_to(a, f"رتبتك بالكروب: {is_admin}\nرتبتك بالبوت: {sender_role}")

# دالة للتحقق من رتبة المستخدم الذي تم الرد على رسالته
def check_user_role(a):
    if a.reply_to_message:
        user_id = a.reply_to_message.from_user.id  
        user_role = get_user_role(user_id)  
        chat_member = bot.get_chat_member(a.chat.id, user_id)  # الحصول على معلومات العضو في الكروب
        
        if chat_member.status in ['administrator', 'creator']:
            is_admin = 'مشرف'
        else:
            is_admin = 'عضو'
        
        bot.reply_to(a, f"رتبته بالكروب: {is_admin}\nرتبته بالبوت: {user_role}")
    else:
        bot.reply_to(a, "يرجى الرد على رسالة مستخدم للتحقق من رتبته.")

# دالة للحصول على عدد الرسائل
def get_user_message_count(user_id):
    return 313  # هذا عدد افتراضي، يمكن تغييره

# دالة لإرسال معلومات المستخدم
def send_user_info(a):
    if a.reply_to_message:
        user = a.reply_to_message.from_user  
    else:
        user = a.from_user  
    user_id = user.id  
    user_name = user.first_name
    user_username = user.username if user.username else "معنده"
    user_role = get_user_role(user_id)  
    user_messages = get_user_message_count(user_id) 
    if user_role not in roles:
        user_role = "مواطن"  
    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ ID ⇢ {user_id}
    ‣ USER ⇢ @{user_username}
    ‣ ROLE ⇢ {user_role}  
    ‣ MESSAGES ⇢ {user_messages}
    ⋆─┄─┄─┄─┄─⋆
    """
    photos = bot.get_user_profile_photos(user.id)

    if photos.total_count > 0:
        bot.send_photo(a.chat.id, photos.photos[0][-1].file_id, caption=message_text)
    else:
        bot.send_message(a.chat.id, message_text)

load_roles()