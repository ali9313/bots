import os
import telebot
import time
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup
import telegram
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)