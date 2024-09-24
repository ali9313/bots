from config import bot
from collections import defaultdict

# قائمة الأعضاء مع رتبهم (التي تم تعريفها في الكود الثاني)
members = defaultdict(lambda: 'عضو')  # افتراضي: عضو

def send_user_info(a):
    user = a.from_user
    user_name = user.first_name
    user_username = user.username if user.username else "معنده"
    user_messages_count = a.message_id
    user_id = user.id  # الحصول على آيدي المستخدم
    user_role = members[user_id]  # التحقق من رتبة المستخدم من القائمة

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