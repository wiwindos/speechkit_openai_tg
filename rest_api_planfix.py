import requests
import json

def text_to_planfix_comment_task(text_from_TextData, task_id):
    # Ваш токен авторизации
    TOKEN = '65d5b3136c990b1f8e9f32311e78fd0b'

    # URL API для добавления комментария к задаче с ID 114
    url = f'https://zevtek.planfix.ru/rest/task/{task_id}/comments/'

    # Заголовки для запроса
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    # Данные для отправки в запросе
    data = {
        "sourceId": "e0c5f3c1-947f-4f29-baa3-d0f7c0b42b47",  # Случайный sourceId
        "sourceObjectId": "c7d1b638-12f5-41f1-b55f-45a28c5efb11",  # Случайный sourceObjectId
        "sourceDataVersion": "AADJIgAAAAA=",
        "dateTime": {
            "date": "12-06-2022",  # Дата комментария
            "time": "12:15",  # Время комментария
            "datetime": "2022-06-12T12:15Z"  # Полная метка времени в формате ISO
        },
        "description": f"{text_from_TextData}",  # Текст комментария
        "owner": {
            "id": "contact:1"  # Установлено на 1
        },
        "isPinned": False,  # Не закреплять комментарий
        "isHidden": False,  # Не скрывать комментарий
        "recipients": {
            "users": [
                {
                    "id": "user:1"  # ID пользователя
                }
            ],
            "roles": []  # Роли (пустой список)
        }
    }

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Проверка результата
    if response.status_code == 200:
        print('Комментарий успешно добавлен')
    else:
        print(f'Ошибка: {response.status_code}, текст ошибки: {response.text}')
