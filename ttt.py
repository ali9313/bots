import logging
from config import *
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ali_json import programmer_ali, owner, creator, owner_id_ali, is_basic_creator, dev, basic_dev

# إعداد logging لتسجيل الأخطاء في ملف log.txt
logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# قاموس لتخزين عدد الرسائل لكل مستخدم في كل دردشة
message_counts = {}

# قاموس لتخزين القوالب الافتراضية
templates = {
    "template1": "<b>المختصر انتِ شي حلو محد يشبهه💕 🫶</b>\n"
                 "<b>الاســم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>\n"
                 "<b>اليـوزر    ⤎  {username}</b>\n"
                 "<b>الايـدي    ⤎ </b> <code>{user_id}</code>\n"
                 "<b>الرتبــه    ⤎ {user_rank} 𓅫</b>\n"
                 "<b>الرسائل  ⤎</b>  {msgs} 💌\n"
                 "<b>التفاعل  ⤎</b>  {stast}\n"
                 "<b>البايـو     ⤎  {bio}</b>\n",
                 
    "template2": "<b>معلومات المستخدم:</b>\n"
                 "<b>الاسم:</b> <a href='tg://user?id={user_id}'>{full_name}</a>\n"
                 "<b>اليزر:</b> {username}\n"
                 "<b>الرتبة:</b> {user_rank}\n"
                 "<b>عدد الرسائل:</b> {msgs}\n"
                 "<b>التفاعل:</b> {stast}\n"
                 "<b>البيو:</b> {bio}\n",
                 
    "template3": "<b>تفاصيل حسابك:</b>\n"
                 "<b>الاسم:</b> <a href='tg://user?id={user_id}'>{full_name}</a>\n"
                 "<b>الرتبة:</b> {user_rank} 𓅫\n"
                 "<b>عدد الرسائل:</b> {msgs} 💌\n"
                 "<b>التفاعل:</b> {stast}\n"
                 "<b>البيو:</b> {bio}\n"
}

# دالة لحساب عدد الرسائل الخاصة بالمستخدم
def get_message_count(user_id, chat_id):
    if chat_id in message_counts:
        return message_counts[chat_id].get(user_id, 0)
    return 0

# دالة للتحقق من رتبة المستخدم
def check_user_rank(user_id, chat_id):
    if programmer_ali(user_id):
        return "مبرمج السورس"
    elif owner(user_id, chat_id):
        return "مالك"
    elif creator(user_id, chat_id):
        return "منشئ"
    elif owner_id_ali(user_id):
        return "مطور اساسي"
    elif is_basic_creator(user_id):
        return "منشئ أساسي"
    elif dev(user_id):
        return "مطور"
    elif basic_dev(user_id):
        return "مطور ثانوي"
    else:
        return "عضو"

# دالة لجلب معلومات المستخدم
def fetch_info(a: Message, selected_template):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        full_name = user.first_name + ' ' + (user.last_name if user.last_name else "")
        user_id = user.id
        username = f"@{user.username}" if user.username else "لا يـوجـد"

        # جلب معلومات البايو باستخدام get_chat
        user_chat = bot.get_chat(user_id)
        user_bio = user_chat.bio if user_chat.bio else "لا يـوجـد"

        # جلب عدد الرسائل الفعلي
        aaa = get_message_count(user_id, a.chat.id)

        # تحديد مستوى التفاعل بناءً على عدد الرسائل
        if aaa < 100: 
            al = "غير متفاعل  🗿"
        elif aaa < 500:
            al = "ضعيف  🗿"
        elif aaa < 700:
            al = "شد حيلك  🏇"
        elif aaa < 1000:
            al = "ماشي الحال  🏄🏻‍♂"
        elif aaa < 2000:
            al = "ملك التفاعل  🎖"
        elif aaa < 3000:
            al = "امبراطور التفاعل  🥇"
        elif aaa < 4000:
            al = "غنبله  💣"
        else:
            al = "نار وشرر  🏆"

        # الحصول على رتبة المستخدم
        user_rank = check_user_rank(user_id, a.chat.id)

        # استخدام الكليشة المختارة
        template = templates[selected_template]

        caption = template.format(
            full_name=full_name,
            username=username,
            user_id=user_id,
            user_rank=user_rank,
            msgs=aaa,
            stast=al,
            bio=user_bio
        )

        return caption
    except Exception as e:
        logging.error("Error in fetch_info function: %s", e)
        return "حدث خطأ أثناء جلب معلومات المستخدم."

# دالة لإرسال صورة الملف الشخصي مع الكابشن
def send_user_info_with_photo(a: Message, selected_template):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        user_id = user.id

        # جلب صورة الملف الشخصي للمستخدم
        photos = bot.get_user_profile_photos(user_id)

        # التحقق من وجود صور للمستخدم
        if photos.total_count > 0:
            # جلب أول صورة من الصور المتاحة
            photo_file_id = photos.photos[0][-1].file_id
            
            # جلب الكابشن (المعلومات) 
            caption = fetch_info(a, selected_template)

            # إرسال الصورة مع الكابشن
            bot.send_photo(a.chat.id, photo_file_id, caption=caption, parse_mode="HTML")
        else:
            # في حالة عدم وجود صورة شخصية، يتم إرسال المعلومات فقط
            caption = fetch_info(a, selected_template)
            bot.send_message(a.chat.id, caption, parse_mode="HTML")

    except Exception as e:
        logging.error("Error in send_user_info_with_photo function: %s", e)
        bot.send_message(a.chat.id, "حدث خطأ أثناء جلب صورة المستخدم.", parse_mode="HTML")

# دالة لحساب عدد الرسائل
def count_messages(a: Message):
    chat_id = a.chat.id
    user_id = a.from_user.id
    if chat_id not in message_counts:
        message_counts[chat_id] = {}
    if user_id in message_counts[chat_id]:
        message_counts[chat_id][user_id] += 1
    else:
        message_counts[chat_id][user_id] = 1

# دالة لإرسال الأزرار لاختيار الكليشة
def send_template_options(a: Message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("تخطي", callback_data="skip"),
        InlineKeyboardButton("تأكيد", callback_data="confirm"),
        InlineKeyboardButton("إلغاء", callback_data="cancel")
    )
    
    # عرض الكليشة الأولى كمحتوى نصي
    initial_caption = fetch_info(a, "template1")  # اختر الكليشة الافتراضية هنا
    bot.send_message(a.chat.id, initial_caption, reply_markup=markup)

# دالة لمعالجة ردود الأزرار
@bot.callback_query_handler(func=lambda call: True)
def handle_template_selection(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if call.data == "skip":
        # تخطي إلى كليشة أخرى
        new_caption = fetch_info(call.message, "template2")  # اختر كليشة أخرى
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=new_caption, parse_mode="HTML")

    elif call.data == "confirm":
        # تأكيد اختيار الكليشة (يمكنك هنا إضافة أي إجراء تريده)
        selected_template = "template1"  # تأكيد الكليشة الأولى
        send_user_info_with_photo(call.message, selected_template)

    elif call.data == "cancel":
        # إلغاء العملية
        bot.send_message(chat_id, "تم إلغاء العملية.", parse_mode="HTML")
