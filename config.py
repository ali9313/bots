import os
import telebot
import time
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)