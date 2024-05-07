import os
import time
from datetime import datetime
from threading import Thread
from telegram_bot import bot, send_request
from audio_converterOGG import convert_ogg, move_to_archive
from toBucketYAcloud import toBucket
from speechkit import speech_to_text
from vsegpt import text_to_chatGPT35_summarize

folder_path_search = 'audio'
folder_path_arch = 'archive'

# Создаем папку "audio\archive", если она еще не создана
if not os.path.exists(folder_path_search):
    os.makedirs(folder_path_search)
if not os.path.exists(folder_path_arch):
    os.makedirs(folder_path_arch)

# Обработчик нажатия на inline кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data.startswith('p_'):
        # Если нажата кнопка "Да", обработаем файл
        file_name = call.data.split('_')[1]
        bot.send_message(call.message.chat.id, f"Файл '{file_name}' будет обработан.")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        #путь до перемещенного файла
        file_path = os.path.join(folder_path_arch, file_name)
        print(file_name)
        # обработка из звука в текст
        object_url = toBucket(file_name, folder_path_search)
        move_to_archive(file_name, folder_path_search, folder_path_arch)
        text = speech_to_text(object_url)
        #bot.send_message(call.message.chat.id, text)

        text_summarize = text_to_chatGPT35_summarize(text)
        bot.send_message(call.message.chat.id, text_summarize)


    elif call.data == "cancel":
        bot.send_message(call.message.chat.id, "Ок, файл не будет обработан.")
        # Добавьте здесь необходимую логику для обработки нажатия кнопки "Нет"
        # Удаляем кнопку "Да" после нажатия
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


# Функция мониторинга папки audio
def monitor_audio_folder():
    while True:
        # Получаем список файлов в папке "audio"
        files = os.listdir(folder_path_search)

        # Проверяем каждый файл
        for file_name in files:
            # Ищем индекс последнего символа "__" в имени файла
            last_double_underscore_index = file_name.rfind("__")

            # Если находим "__", извлекаем часть строки после него (телефонный номер)
            if last_double_underscore_index != -1:
                phone_number_start = last_double_underscore_index + 2
                phone_number_end = phone_number_start + 11  # Длина номера телефона 11 символов
                phone_number = file_name[phone_number_start:phone_number_end]

                # Берем последние 4 цифры из телефонного номера
                last_four_digits = phone_number[-4:]

                # Получаем расширение исходного файла
                _, extension = os.path.splitext(file_name)

                # Получаем текущее время (часы и минуты)
                current_time = datetime.now().strftime("%d%m%Y-%H-%M")

                # Формируем новое имя файла с телефонным номером, текущим временем и расширением
                file_new_name = f"{phone_number}-{current_time}{extension}"

                # Формируем полный путь к новому файлу
                new_file_path = os.path.join(folder_path_search, file_new_name)

                # Переименовываем файл
                file_path = os.path.join(folder_path_search, file_name)
                os.rename(file_path, new_file_path)
                file_name = file_new_name

                print("Новое имя файла:", file_name)

            # Проверяем, является ли файл аудиофайлом
            if file_name.endswith(".amr"):

                file_name_ogg = convert_ogg(file_name, path_for_conversion = folder_path_search)

                # Отправляем запрос на обработку файла в Telegram
                send_request(file_name_ogg)

            #elif file_name.endswith(".ogg"):
            #    send_request(file_name)

        time.sleep(5)  # Проверяем папку каждые 5 секунд

# Запускаем мониторинг папки в отдельном потоке
folder_monitor_thread = Thread(target=monitor_audio_folder)
folder_monitor_thread.start()

# Запускаем обработку команд телеграм-бота
bot.infinity_polling()
