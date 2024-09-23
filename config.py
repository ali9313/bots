import os
import telebot
import time
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)