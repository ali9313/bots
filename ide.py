import logging
from config import *
from telebot.types import Message

# إعداد logging لتسجيل الأخطاء في ملف log.txt
logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# دالة لجلب معلومات الإنشاء
def zzz_info(a: Message):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
        user_id = user.id
        username = f"@{user.username}" if user.username else "لا يـوجـد"
        
        # هنا يجب استدعاء الدالة fetch_zelzal لجلب تاريخ الإنشاء (يمكن استبدالها ببيانات ثابتة للاختبار)
        zelzal_sinc = "2023-01-01"  # استبدال هذه القيمة بالدالة الفعلية

        ZThon = f'<a href="T.me/ZThon">ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗮𝘁𝗮 📟</a>'
        ZThon += f"\n<b>⋆─┄─┄─┄─┄─┄─┄─⋆</b>\n\n"
        ZThon += f"<b>• معلومـات إنشـاء حسـاب تيليجـرام 📑 :</b>\n"
        ZThon += f"<b>- الاسـم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>"
        ZThon += f"\n<b>- الايــدي   ⤎ </b> <code>{user_id}</code>"
        ZThon += f"\n<b>- اليـوزر    ⤎  {username}</b>\n"
        ZThon += f"<b>- الإنشـاء   ⤎</b>  {zelzal_sinc}  🗓"
        return ZThon
    except Exception as e:
        logging.error("Error in zzz_info function: %s", e)
        return "حدث خطأ أثناء جلب معلومات الإنشاء."

# دالة لجلب معلومات المستخدم
def fetch_info(a: Message):
    try:
        user = a.reply_to_message.from_user if a.reply_to_message else a.from_user
        full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
        user_id = user.id
        username = f"@{user.username}" if user.username else "لا يـوجـد"
        
        # مثال ثابت لتاريخ الإنشاء (يمكنك تعديل fetch_zelzal لاستخدام تاريخ حقيقي)
        zelzal_sinc = "2023-01-01"
        
        # بيانات إضافية للمستخدم
        user_bio = "لا يـوجـد" if not user.bio else user.bio
        zzz = 500  # هذا العدد يجب أن يمثل عدد الرسائل (يمكنك استدعاء دالة لإحضار العدد الفعلي)
        common_chat = 5  # عدد المجموعات المشتركة
        
        ZED_TEXT = "•⎚• مـعلومـات المسـتخـدم مـن بـوت زدثــون"
        ZEDM = "✦ "
        ZEDF = "⋆─┄─┄─┄─ ᶻᵗʰᵒᶰ ─┄─┄─┄─⋆"
        
        caption = f"<b>{ZED_TEXT} </b>\n"
        caption += f"ٴ<b>{ZEDF}</b>\n"
        caption += f"<b>{ZEDM}الاســم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>"
        caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
        caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{ZEDM}الرتبــه    ⤎ العضو 𓅫 </b>\n"
        caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz} 💌\n"
        caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
        caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zelzal_sinc}  🗓\n" 
        caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
        return caption
    except Exception as e:
        logging.error("Error in fetch_info function: %s", e)
        return "حدث خطأ أثناء جلب معلومات المستخدم."

def send_zzz_info(a: Message):
    zzz_message = zzz_info(a)
    bot.send_message(a.chat.id, zzz_message, parse_mode="HTML")

def send_user_info(a: Message):
    info_message = fetch_info(a)
    bot.send_message(a.chat.id, info_message, parse_mode="HTML")