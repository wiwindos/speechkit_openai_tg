# telegram_bot.py

import os
import time
from telebot import TeleBot #pip install pyTelegramBotAPI
from telebot import types
from config import get_token_telegram, get_user_id_telegram
from call_transcript import get_analysis_result_by_AnalysisResults
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
    btn_no = types.InlineKeyboardButton("Нет", callback_data=f"cancel_{file_name}")
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

        analysis_from_AnalysisResult = get_analysis_result_by_AnalysisResults(audio_file_id)
        if analysis_from_AnalysisResult == None:
            bot.send_message(message.chat.id, "Попробуйте еще раз")
            bot.register_next_step_handler(message, send_request_idTaskPlanfix)
        else:
            bot.send_message(message.chat.id, "ID задачи успешно получен. И сообщение отправлено в Planfix")
            text_to_planfix_comment_task(analysis_from_AnalysisResult, task_id)

    except ValueError:
        bot.send_message(message.chat.id,
                         "Пожалуйста, введите корректный ID задачи (тип integer). Попробуйте еще раз.")
        bot.register_next_step_handler(message, send_request_idTaskPlanfix)

def split_message_by_words(text, max_length=4096):
    # Разделяем текст на слова
    words = text.split(' ')
    messages = []
    current_message = ""

    for word in words:
        # Если текущее слово помещается в сообщение, добавляем его
        if len(current_message) + len(word) + 1 <= max_length:
            current_message += word + ' '
        else:
            # Если сообщение достигает лимита, отправляем его
            messages.append(current_message.strip())
            current_message = word + ' '

    # Добавляем последнее сообщение, если оно не пустое
    if current_message:
        messages.append(current_message.strip())

    return messages

# Обработчик команды /start и /help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для обработки аудиофайлов. Жду новых файлов в папке 'audio'.")