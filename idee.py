from config import bot

def send_user_info(a):
    user = a.from_user
    user_name = user.first_name
    user_username = user.username if user.username else "معنده"
    user_messages_count = a.message_id

    message_text = f"""
    ⋆─┄─┄─┄─┄─⋆
    ‣ NAME ⇢ {user_name}
    ‣ USER ⇢ @{user_username}
    ‣ MESSAGE ⇢ {user_messages_count}
    ⋆─┄─┄─┄─┄─⋆
    """

    photos = bot.get_user_profile_photos(user.id)

    if photos.total_count > 0:
        bot.send_photo(a.chat.id, photos.photos[0][-1].file_id, caption=message_text)
    else:
        bot.send_message(a.chat.id, message_text)