# -*- coding: utf-8 -*-

#3 распознаем из хранилища

import requests
import time
import json

def speech_to_text(filelink):
    # Укажите ваш IAM-токен и ссылку на аудиофайл в Object Storage.
    key = '<>'
    #filelink = 'https://buket.storage.yandexcloud.net/file'

    POST ='https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize'

    body ={
        "config": {
            "specification": {
                "languageCode": "ru-RU"
            }
        },
        "audio": {
            "uri": filelink
        }
    }

    header = {'Authorization': 'Api-Key {}'.format(key)}

    # Отправьте запрос на распознавание.
    req = requests.post(POST, headers=header, json=body)
    data = req.json()
    print(data)

    id = data['id']

    # Запрашивайте на сервере статус операции, пока распознавание не будет завершено.
    while True:

        time.sleep(1)

        GET = "https://operation.api.cloud.yandex.net/operations/{id}"
        req = requests.get(GET.format(id=id), headers=header)
        req = req.json()

        if req['done']: break
        print("Not ready")

    # Покажите только текст из результатов распознавания.
    text = ""
    for chunk in req['response']['chunks']:
        text += chunk['alternatives'][0]['text']

    # Выводим текст
    print("Text:")
    print(text)
    return text
"""
    # Покажите полный ответ сервера в формате JSON.
    print("Response:")
    print(json.dumps(req, ensure_ascii=False, indent=2))

    # Покажите только текст из результатов распознавания.
    print("Text chunks:")
    for chunk in req['response']['chunks']:
        print(chunk['alternatives'][0]['text'])"""

