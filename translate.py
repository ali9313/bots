from config import *
import requests

def translate(text, source_lang='auto', target_lang='ar'):
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&dt=t'
    params = {
        'sl': source_lang,
        'tl': target_lang,
        'q': text
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, data=params, headers=headers)
    if response.status_code == 200:
        sentences_array = response.json()[0]
        sentences = ''.join([s[0] for s in sentences_array if s[0]])
        return sentences
    else:
        return "حدث خطأ: لم نتمكن من ترجمة النص."
def handle_translation(a):
    # التحقق من أن المستخدم قام بالرد على رسالة
    if a.reply_to_message:
        # الحصول على نص الرسالة التي تم الرد عليها
        text_to_translate = a.reply_to_message.text
        
        # ترجمة النص
        translated_text = translate(text_to_translate)
        
        # إرسال النص المترجم
        bot.send_message(a.chat.id, translated_text, reply_to_message_id=a.message_id)
    else:
        bot.send_message(a.chat.id, "يرجى الرد على رسالة تحتوي على النص الذي ترغب بترجمته.", reply_to_message_id=a.message_id)
