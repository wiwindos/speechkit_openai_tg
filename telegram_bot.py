# telegram_bot.py

import os
import time
from telebot import TeleBot #pip install pyTelegramBotAPI
from telebot import types
from config import get_token_telegram, get_user_id_telegram
from call_transcript import get_text_by_audioFileId
from rest_api_planfix import text_to_planfix_comment_task

# Инициализация Telegram Bot
bot = TeleBot(get_token_telegram())

# ID пользователя, которому будет отправлен запрос на обработку файла
user_id = get_user_id_telegram()

# Функция для отправки запроса пользователю в Telegram Bot
def send_request(file_name: str, audio_file_id_insql: int) -> None:
    # Создаем клавиатуру с inline кнопками "Да" и "Нет"
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("Да", callback_data=f"p_{file_name}_{audio_file_id_insql}")
    btn_no = types.InlineKeyboardButton("Нет", callback_data="cancel")
    keyboard.add(btn_yes, btn_no)

    bot.send_message(user_id, f"Хотите обработать файл '{file_name}'?", reply_markup=keyboard)

def send_Task_komment_Planfix(text_summarize: str , audio_file_id_insql: int) -> None:
    # Создаем клавиатуру с inline кнопками "Выслать в Planfix?"
    keyboard = types.InlineKeyboardMarkup()
    btn_send = types.InlineKeyboardButton("Выслать в PF", callback_data=f"sp_{audio_file_id_insql}")
    keyboard.add(btn_send)

    bot.send_message(user_id, f"{text_summarize}", reply_markup=keyboard)

def send_request_idTaskPlanfix(message) -> int:
    try:
        task_id_str = message.text.split('_')[0]
        audio_file_id = message.text.split('_')[1]
        task_id = int(task_id_str)  # Преобразуем ввод в integer
        #id_connect(task_id)  # Вызов вашей функции с ID задачи

        text_from_TextData = get_text_by_audioFileId(audio_file_id)
        if text_from_TextData == None:
            bot.send_message(message.chat.id, "Попробуйте еще раз")
            bot.register_next_step_handler(message, send_request_idTaskPlanfix)
        else:
            bot.send_message(message.chat.id, "ID задачи успешно получен.")
            text_to_planfix_comment_task(text_from_TextData, task_id)

    except ValueError:
        bot.send_message(message.chat.id,
                         "Пожалуйста, введите корректный ID задачи (тип integer). Попробуйте еще раз.")
        bot.register_next_step_handler(message, send_request_idTaskPlanfix)


# Обработчик команды /start и /help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для обработки аудиофайлов. Жду новых файлов в папке 'audio'.")