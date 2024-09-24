from config import bot
from collections import defaultdict

# قائمة الأعضاء مع رتبهم (التي تم تعريفها في الكود الثاني)
members = defaultdict(lambda: 'عضو')  # افتراضي: عضو

# دالة للتحقق من رتبة المستخدم
def get_user_role(user_id):
    return members[user_id]

def send_user_info(a):
    # إذا كان المستخدم يرد على شخص آخر
    if a.reply_to_message:
        user = a.reply_to_message.from_user  # الحصول على معلومات الشخص المُرد عليه
    else:
        user = a.from_user  # الحصول على معلومات الشخص الذي أرسل الأمر

    user_name = user.first_name
    user_username = user.username if user.username else "معنده"
    user_messages_count = a.message_id
    user_id = user.id  # الحصول على آيدي المستخدم

    # التحقق من رتبة المستخدم من خلال الكود الثاني
    user_role = get_user_role(user_id)

    # إنشاء الكليشة مع الرتبة
    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ ID ⇢ {user_id}
    ‣ USER ⇢ @{user_username}
    ‣ RANK ⇢ {user_role}
    ‣ MESSAGE ⇢ {user_messages_count}
    ⋆─┄─┄─┄─┄─⋆
    """

    # جلب الصورة الشخصية للمستخدم إذا كانت متاحة
    photos = bot.get_user_profile_photos(user.id)

    if photos.total_count > 0:
        bot.send_photo(a.chat.id, photos.photos[0][-1].file_id, caption=message_text)
    else:
        bot.send_message(a.chat.id, message_text)