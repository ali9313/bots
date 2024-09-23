from config import *

def send_user_info(a):
    user = a.from_user
    user_name = user.first_name
    user_username = user.username if user.username else "لا يوجد"
    user_messages_count = a.message_id
    bot.send_message(a.chat.id, message_text)
    photos = bot.get_user_profile_photos(user.id)
    
    if photos.total_count > 0:
        bot.send_photo(a.chat.id, photos.photos[0][-1].file_id)
    else:
        bot.reply_to(a, "لا توجد صورة بروفايل.")

