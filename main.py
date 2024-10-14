import os
import time
import re
from datetime import datetime
from threading import Thread
from telegram_bot import bot, send_request, send_Task_komment_Planfix, send_request_idTaskPlanfix, split_message_by_words
from audio_converterOGG import convert_ogg, move_to_archive, get_audio_duration
from toBucketYAcloud import toBucket
from speechkit import speech_to_text
from vsegpt import text_to_chatGPT35_summarize
from call_transcript import add_data_to_audio_files, add_text_data, add_analysis_result
from yandexGPTtest import text_to_yandexGPT_summarize

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
        audio_file_id_insql = call.data.split('_')[2]
        bot.send_message(call.message.chat.id, f"Файл '{file_name}' будет обработан.")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        #путь до перемещенного файла
        file_path = os.path.join(folder_path_arch, file_name)
        print(file_name)

        # обработка из звука в текст
        object_url = toBucket(file_name, folder_path_search)
        move_to_archive(file_name, folder_path_search, folder_path_arch)
        text = speech_to_text(object_url)

        messages = split_message_by_words(text)
        for message in messages:
            text = text + " " + message
            bot.send_message(call.message.chat.id, message)
        #bot.send_message(call.message.chat.id, text + "       ")

        #занесение в бд TextData
        current_time_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text_data_file_id = add_text_data(text, audio_file_id_insql, current_time_date)

        #text_summarize = text_to_chatGPT35_summarize(text)
        text_summarize = text_to_yandexGPT_summarize(text)

        #text_summarize = "NONE"

        # занесение в бд AnalysisResults
        add_analysis_result(text_data_file_id, text_summarize, current_time_date)

        #bot.send_message(call.message.chat.id, text_summarize)
        send_Task_komment_Planfix(text_summarize, text_data_file_id)

    elif call.data == "cancel":
        bot.send_message(call.message.chat.id, "Ок, файл не будет обработан.")
        # Удаляем кнопку "Да" после нажатия
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    elif call.data.startswith('sp_'):
        # Если нажата кнопка "Выслать в PF", запрос у пользователя ID Task Planfix
        text_data_file_id = call.data.split('_')[1]
        bot.send_message(call.message.chat.id, "Пожалуйста, введите ID задачи Planfix:" + f"Через _ введите '{text_data_file_id}'")
        bot.register_next_step_handler(call.message, send_request_idTaskPlanfix)

# Функция мониторинга папки audio
def monitor_audio_folder():
    while True:
        # Получаем список файлов в папке "audio"
        files = os.listdir(folder_path_search)

        # Проверяем каждый файл
        for file_name_o in files:
            file_name = file_name_o.replace("-", "")
            file_name = file_name.replace(" ", "")

            #print(file_name)
            phone_pattern = re.compile(r'(\d{10,})\.amr')
            match = phone_pattern.search(file_name)



            if match:
                phone_number = match.group(1)

                # Берем последние 4 цифры из телефонного номера
                last_four_digits = phone_number[-4:]

                # Получаем расширение исходного файла
                _, extension = os.path.splitext(file_name)

                # Получаем текущее время (часы и минуты)
                current_time_minsec = datetime.now().strftime("%d%m%Y-%H-%M-%S")

                # Формируем новое имя файла с телефонным номером, текущим временем и расширением
                file_new_name = f"{phone_number}-{current_time_minsec}{extension}"

                # Формируем полный путь к новому файлу
                new_file_path = os.path.join(folder_path_search, file_new_name)

                # Переименовываем файл
                file_path = os.path.join(folder_path_search, file_name_o)
                os.rename(file_path, new_file_path)
                file_name = file_new_name

                print("Новое имя файла:", file_name)
            else:
                if file_name.endswith(".ogg"):
                    #print("в папке только файлы с расширением .ogg")
                    continue
                else:
                    #print("номер телефона в названии файла не найден")
                    continue

            # Проверяем, является ли файл аудиофайлом
            if file_name.endswith(".amr"):
                duration = get_audio_duration(f'{folder_path_search}/{file_name}')
                if duration is None:
                    print("Что то случилось на этапе определения длительности, код приостановлен")
                    continue

                file_name_ogg = convert_ogg(file_name, path_for_conversion=folder_path_search)
                current_time_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # занесение в бд AudioFiles
                audio_file_id_insql = add_data_to_audio_files(phone_number, current_time_date, duration,
                                                              f'{folder_path_search}/{file_name_ogg}')

                # Отправляем запрос на обработку файла в Telegram
                send_request(file_name_ogg, audio_file_id_insql)

            time.sleep(3)

        time.sleep(5)  # Проверяем папку каждые 5 секунд

# Запускаем мониторинг папки в отдельном потоке
folder_monitor_thread = Thread(target=monitor_audio_folder)
folder_monitor_thread.start()

# Запускаем обработку команд телеграм-бота
bot.infinity_polling()
