import os
import telebot
import time
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup
from telebot import TeleBot
from collections import defaultdict
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)