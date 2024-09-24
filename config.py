import os
import telebot
import time
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup
from telebot import Bot, Update, CommandHandler, MessageHandler, Filters
from collections import defaultdict
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)