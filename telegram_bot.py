# telegram_bot.py

import os
import time
from telebot import TeleBot #pip install pyTelegramBotAPI
from telebot import types

# Инициализация Telegram Bot
bot = TeleBot("<>")

# ID пользователя, которому будет отправлен запрос на обработку файла
user_id = 148918255

# Функция для отправки запроса пользователю в Telegram Bot
def send_request(file_name):
    # Создаем клавиатуру с inline кнопками "Да" и "Нет"
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("Да", callback_data=f"process_{file_name}")
    btn_no = types.InlineKeyboardButton("Нет", callback_data="cancel")
    keyboard.add(btn_yes, btn_no)

    bot.send_message(user_id, f"Хотите обработать файл '{file_name}'?", reply_markup=keyboard)


# Обработчик команды /start и /help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для обработки аудиофайлов. Жду новых файлов в папке 'audio'.")