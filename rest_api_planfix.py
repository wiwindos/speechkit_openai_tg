import requests
import json
from config import get_api_key_planfix, get_url_planfix
from datetime import datetime, timedelta

def text_to_planfix_comment_task(text_from_TextData, task_id):
    # Ваш токен авторизации
    TOKEN = get_api_key_planfix()

    # URL API для добавления комментария к задаче
    myUrl = get_url_planfix()
    url = f'{myUrl}/{task_id}/comments/'

    # Заголовки для запроса
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    # Данные для отправки в запросе
    current_time_utc_plus_5 = datetime.utcnow()
    data = {
        "sourceId": "e0c5f3c1-947f-4f29-baa3-d0f7c0b42b47",  # Случайный sourceId
        "sourceObjectId": "c7d1b638-12f5-41f1-b55f-45a28c5efb11",  # Случайный sourceObjectId
        "sourceDataVersion": "AADJIgAAAAA=",
        "dateTime": {
            "date": current_time_utc_plus_5.strftime("%d-%m-%Y"),  # Дата комментария
            "time": current_time_utc_plus_5.strftime("%H:%M"),  # Время комментария
            "datetime": current_time_utc_plus_5.strftime("%Y-%m-%dT%H:%MZ")  # Полная метка времени в формате ISO
        },
        "description": f"{text_from_TextData}",  # Текст комментария
        "owner": {
            "id": "1"  # Установлено на 1
        },
        "isPinned": False,  # Не закреплять комментарий
        "isHidden": False,  # Не скрывать комментарий
        "recipients": {
            "users": [
                {
                    "id": "user:1"  # ID пользователя
                }
            ],
            "roles": [
                "admin"
            ]  # Роли (пустой список)
        }
    }

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Проверка результата
    if response.status_code == 200:
        print('Комментарий успешно добавлен')
    else:
        print(f'Ошибка: {response.status_code}, текст ошибки: {response.text}')
