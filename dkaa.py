import requests
from config import *

def chat_with_gpt(a):
    user_input = a.text[len("بوت "):]  # الحصول على السؤال بعد كلمة "بوت"
    api_url = f"http://ttrtt.serv00.net/API/it_bero.php?promt={user_input}"
    response = requests.get(api_url)

    if response.status_code == 200:
        gpt_response = response.text
    else:
        gpt_response = "عذرًا، لم أستطع الحصول على رد من API."

    bot.reply_to(a, f"<b>{gpt_response}</b>", parse_mode='HTML')