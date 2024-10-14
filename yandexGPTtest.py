import requests
import json
from config import get_modelUri_yandexGPT
from config import get_apikey_yandexGPT

def text_to_yandexGPT_summarize(text_incoming: str) -> str:
    modelUri = get_modelUri_yandexGPT()
    prompt = {
        "modelUri": f'{modelUri}',
        "completionOptions": {
            "stream": False,
            "temperature": 0,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Шаг 1: Определение принадлежности фраз "
                        "Определи, кому принадлежит каждая фраза: менеджеру по продажам или клиенту. Для этого обозначь начало каждой реплики соответствующими метками: Менеджер и Клиент. "
                        "Шаг 2: Очистка текста и исправление ошибок "
                        'Удали слова-паразиты (например, ну, как бы, типа и т.д.). Исправь ошибки, возникшие в результате автоматического распознавания речи, чтобы текст был грамматически корректным и легко читаемым. Убедись, что основная суть каждого предложения передана правильно и точно.'
                        "Шаг 3: Краткое изложение звонка"
                        "В одном абзаце изложи основные тезисы диалога: ключевые вопросы клиента, предложения менеджера, обсуждаемые решения и важные моменты, которые стороны упомянули в ходе разговора."
                        "Ключевые моменты: Выдели список ключевых моментов, которые были обсуждены, например, продуктовые особенности, сроки поставки, цены, дополнительные услуги и т.д."
                        "Следующие шаги:"
                        "Перечисли конкретные действия или следующие шаги, которые стороны согласовали в ходе звонка (например, отправка коммерческого предложения, организация встречи, демонстрация продукта и т.д.), не ."
                        "Не выводи в ответе результат шагов 1,2, только 3 как можно подробнее, на основе этого будет вестись дальнейшая работа с клиентом. Не придумывай ничего - тебя проверят."
            },
            {
                "role": "user",
               # "text": "Добрый день! Компания Red Flag, монитор Александр. Предлагаем вам свои услуги по очистке логины и трубы в час. Очень интересуюсь. Спасибо. Спасибо большое. Игорь Сергеевич, да, доброе утро. Слушай, скажи, мы сейчас как раз занимаемся контрольной процедурой, да? Так. Ну, заявочку заправляем на контроль, да? Угу. А у вас сам, как я понял, уже у самих себя есть наличие? Ну, у нас будет до конца мая. До конца апреля, точнее. А паспорт и что? Ну, можно, а зачем? Что вы занимаетесь? Что за тендер? Куда, чего, зачем? Ну, мы уже разговаривали с тобой по обследованию трупа. А, двигается куда-то его просто. Да. На площадке появился. Сейчас надо просто туда податься. А сможете скинуть? Можете мне скинуть уже ссылочку? Как? Не могу тебе ссылочку скинуть, потому что это... Ну, она же получит деньги за это, и она... Ну, ты сам понимаешь. Там, вот эта процедура, она, получается, себе... Ну, чтобы туда зайти на площадку, у нас бы и ссылочка была. Не могу скинуть. Как-то не договариваюсь, зачем могу скинуть. Ну, я понимаю, у нас вроде и оплачено. Ну, коль. Не знаю такого числа, но, да, да, должно было оплачено. Там надо? Ну, я посмотрю. Ну, я просто ознакомлюсь, что они там выложили-то. Хоть какую документацию. Что они там хотят. Вы можете выставить просто документацию, выгрузить и скинуть мне, я ознакомлюсь, о чем речь идет. Какие они там объемы-то рассматривают по итогу? Маленькие. Ну, сколько? Сейчас скажу. Можно сказать, что 60. 5163. Интересно. Полторы стало. Опять большое стало. Интересно, это у них опрос цен уже еще или уже тендер? Тендер. Тендер. Вот я отбил тендер. Закрасил. Смотрел. Что нам делать? Интересно. Интересно. 5863. А мы посылали на полтора тысяча. Там было 1400, да? Да. Да, да, да. На 1400 почти. Да. Странная еребенка. Угу. Ладно, я понял тебя. Я скинул что-нибудь? Скиньте, да. Скиньте, пожалуйста. Можно и документацию, и ссылочку. Я вам скинул. Что нужно? Паспорт? А? Я ссылочку никак не скинул. Нет ссылки. А, ну ладно. Я сейчас посылаю. Ссылку-то беру, она все равно за ток свежая. Я тебе могу ее скинуть, а пароля-то нету. Чего толком? Почему? Все есть. Ну, тогда выходи, посылай пароль. Ну, хорошо. Ну, хорошо. Я тебе очень хорошо. Я же передам свой пароль. Нет, понятно, конечно. Нет, у нас есть доступ. Мы же участвуем тоже на Луковской площадке. Где они разместили-то? У себя на сайте? Да. Хорошо, посмотрим. От меня-то что требуется на данный момент? Ну, паспорт кто-то у вас по оборудованию проиграл. Паспорт. Будет паспорт. Что-то еще? Пока все. Пока все. Остальное у меня все есть, кроме паспорта. Угу. Ладно, сейчас я знакомлюсь тоже с документацией. Что там вообще есть. Согласуемся. Хорошо? Приехал Сергей? Да, приехал. Отлично. Угу. Угу. Угу. Угу. Угу. Слушаю. Добрый день, компания Кредиен, слушаю вас. Как могу к вам обращаться? Александр. Александр. Меня Евгений зовут. Я не услышал, у вас как называется предприятие, может завод какой? Ивановская область, город Родники. Родниковский завод. Занимаемся металлоконструкцией крановой. У нас есть стационарный анализатор. Но для того, чтобы в 100% все листы не проверить, потому что мало ли какая-то ресурс. И речь идет по плану анализатора. Что я хотел сказать, что я в своей мысли ушел. Смотрите, у нас регинофлюоресцентный анализатор под нашим брендом выпускается. Является средством измерения. Под черные металлы они подходят, наверное, не на 100%. Стоимость них вилка центита 2-3 миллиона. Совсем черные стали, типа сталь 3, сталь 20. Не для черных металлов. Они не определяют углерод. Все остальные лигирующие элементы, включая серый фосфор, определяют. Углерод там нужно. А вообще есть такие расстояния, занимающиеся углеродом? Есть. Вам нужен максимально портативный вариант? Или на колесиках, возможно? Ну, портативный, портативный. Желательно, чтобы листы не резались. Сейчас у нас есть нормальный анализатор стационарный. Но приходится листом отрезать уголочек. Потом его вырабатывать. Измерение на улице. В основном в помещении. Хорошо, я понял вас. Вам нужен прибор, черный металл измерять, не отрезая образцы. Подготовку не производить. У нас... Есть сомнения? Нет. Да, но получили мы уже детский металл. И есть сомнения. Ну, допустим, пачка распечатанная. А все листы такой стали. Не дай Бог попадется какой-то в другой сталь. Да, чтобы не было пересортиться. Я понял вас. Мы вам можем предложить мобильный. На колесиках с аргоном. Его можно перевозить в пределах цеха. У него выносной датчик. То есть листы металла не надо отрезать. То есть у вас пришел лист. Просто углерод измерить качественно можно только в среде инертной. Именно в аргоне. Если рассматривать какие-нибудь лазерные. Они более портативные. С достаточно большой погрешностью. То есть, допустим, сталь 20, сталь 40. У него порядок цены 2-2,8 млн. В зависимости от калибровок. Как я понимаю, у вас какие типичные марки? Сталь 20, сталь 3, 0,9, 2С. Мы в Баррексе много используем. Но это уже проблем. Это кругляк. Это в основном низ коллегированных, правильно? Каких-то нержавеек нет? Нержавейка есть? Нержавейка есть. Она не идет на сварный металл конструкции. Мы его на стандартном. У нас есть проблема. Как говорится, сварная металл конструкция. Если где-то попадет центральная сталь. Большое задержание углерода. Запутали на базе. И мы ее варим. Решить вот такую опасность. А если, например, сколько-то лицов пачкать? Какая гарантия? Да, Александр, я понял вашу задачу. У вас, получается, ответственные детали, которые нужно контролировать. Даже 100% на входном контроле. Да. Там и нержавейки. Там у нас и бронза, латунь. Все определяется. То есть вам нужно только одну задачу закрыть. Это черные металлы. Цветные, в принципе, вы можете и на стационаре. Да, да. Вот только черный металл не коллектированный. Чтобы было коллектировано. Хорошо. Может быть, там. Например, сальт. Например, сальт-3. Сальт-35, сальт-40. Сальт-20, сальт-09. Если где-то там кто-то запутает, если нам попадет сальт-45, то обычно металлургия варит какой-то кран большой. Значит, там может попасть. Да, но у вас очень ответственные детали. Мы решим на 100% согласно ГОСТ. Точность будет не хуже, чем ваша стационарная. Как я могу вам коммерческое предложение сделать? Может, сможете мне продиктовать почту или отправить на WhatsApp? Вы предлагаете? Это имеется в виду переносные на колесиках? Вам лазерные, мобильные? Есть просто еще один метод, но там большие погрешности. Сталь, допустим, 30 от стали 40, вы не различите, потому что погрешность высокая. Это к вам не подходит, поэтому я вам даже не предлагаю этот метод. Вам нужно остановиться только на оптико-эмиссионном, но мобильном комплексе. Вот. Да, у вас какой-то бюджет есть? Бюджет-то какой у вас? Бюджет какой у вас? Давайте, Александр, я вам коммерческое предложение выставлю, чтобы вы не с пустыми руками шли к руководству, и отчего вам надо было отталкиваться, потому что в любом случае можно и скидки, и так далее рассмотреть, лизинг там. Давайте. М? Да. Так. Записал. Это придет к вам, да? Александр, хорошо. А у вас какая должность? Ну, начальство следовательского отдела. Ну, хотя бы до соответствующей лицензии будем идти. Хорошо, ну я вам по максимуму информации скину коммерческое предложение. Вот этот номер телефона у вас прямой, да? 6807. Хорошо, хорошо. Все, направим вам. Спасибо. До свидания."
                "text": f'{text_incoming}'
            }


            # {
            #     "role": "system",
            #     "text": "Ты менеджер по продажам в сегменте 2b2. Ты звонишь клиенту по телефону и у вас возникает диалог. По итогу тебе необходимо получить сжатый пересказ диалога по пунктам 1. 2. 3."
            # },
            # {
            #     "role": "user",
            #     "text": "Добрый день! Компания Red Flag, монитор Александр. Предлагаем вам свои услуги по очистке логины и трубы в час. Очень интересуюсь. Спасибо. Спасибо большое. Игорь Сергеевич, да, доброе утро. Слушай, скажи, мы сейчас как раз занимаемся контрольной процедурой, да? Так. Ну, заявочку заправляем на контроль, да? Угу. А у вас сам, как я понял, уже у самих себя есть наличие? Ну, у нас будет до конца мая. До конца апреля, точнее. А паспорт и что? Ну, можно, а зачем? Что вы занимаетесь? Что за тендер? Куда, чего, зачем? Ну, мы уже разговаривали с тобой по обследованию трупа. А, двигается куда-то его просто. Да. На площадке появился. Сейчас надо просто туда податься. А сможете скинуть? Можете мне скинуть уже ссылочку? Как? Не могу тебе ссылочку скинуть, потому что это... Ну, она же получит деньги за это, и она... Ну, ты сам понимаешь. Там, вот эта процедура, она, получается, себе... Ну, чтобы туда зайти на площадку, у нас бы и ссылочка была. Не могу скинуть. Как-то не договариваюсь, зачем могу скинуть. Ну, я понимаю, у нас вроде и оплачено. Ну, коль. Не знаю такого числа, но, да, да, должно было оплачено. Там надо? Ну, я посмотрю. Ну, я просто ознакомлюсь, что они там выложили-то. Хоть какую документацию. Что они там хотят. Вы можете выставить просто документацию, выгрузить и скинуть мне, я ознакомлюсь, о чем речь идет. Какие они там объемы-то рассматривают по итогу? Маленькие. Ну, сколько? Сейчас скажу. Можно сказать, что 60. 5163. Интересно. Полторы стало. Опять большое стало. Интересно, это у них опрос цен уже еще или уже тендер? Тендер. Тендер. Вот я отбил тендер. Закрасил. Смотрел. Что нам делать? Интересно. Интересно. 5863. А мы посылали на полтора тысяча. Там было 1400, да? Да. Да, да, да. На 1400 почти. Да. Странная еребенка. Угу. Ладно, я понял тебя. Я скинул что-нибудь? Скиньте, да. Скиньте, пожалуйста. Можно и документацию, и ссылочку. Я вам скинул. Что нужно? Паспорт? А? Я ссылочку никак не скинул. Нет ссылки. А, ну ладно. Я сейчас посылаю. Ссылку-то беру, она все равно за ток свежая. Я тебе могу ее скинуть, а пароля-то нету. Чего толком? Почему? Все есть. Ну, тогда выходи, посылай пароль. Ну, хорошо. Ну, хорошо. Я тебе очень хорошо. Я же передам свой пароль. Нет, понятно, конечно. Нет, у нас есть доступ. Мы же участвуем тоже на Луковской площадке. Где они разместили-то? У себя на сайте? Да. Хорошо, посмотрим. От меня-то что требуется на данный момент? Ну, паспорт кто-то у вас по оборудованию проиграл. Паспорт. Будет паспорт. Что-то еще? Пока все. Пока все. Остальное у меня все есть, кроме паспорта. Угу. Ладно, сейчас я знакомлюсь тоже с документацией. Что там вообще есть. Согласуемся. Хорошо? Приехал Сергей? Да, приехал. Отлично. Угу. Угу. Угу. Угу. Угу. Слушаю. Добрый день, компания Кредиен, слушаю вас. Как могу к вам обращаться? Александр. Александр. Меня Евгений зовут. Я не услышал, у вас как называется предприятие, может завод какой? Ивановская область, город Родники. Родниковский завод. Занимаемся металлоконструкцией крановой. У нас есть стационарный анализатор. Но для того, чтобы в 100% все листы не проверить, потому что мало ли какая-то ресурс. И речь идет по плану анализатора. Что я хотел сказать, что я в своей мысли ушел. Смотрите, у нас регинофлюоресцентный анализатор под нашим брендом выпускается. Является средством измерения. Под черные металлы они подходят, наверное, не на 100%. Стоимость них вилка центита 2-3 миллиона. Совсем черные стали, типа сталь 3, сталь 20. Не для черных металлов. Они не определяют углерод. Все остальные лигирующие элементы, включая серый фосфор, определяют. Углерод там нужно. А вообще есть такие расстояния, занимающиеся углеродом? Есть. Вам нужен максимально портативный вариант? Или на колесиках, возможно? Ну, портативный, портативный. Желательно, чтобы листы не резались. Сейчас у нас есть нормальный анализатор стационарный. Но приходится листом отрезать уголочек. Потом его вырабатывать. Измерение на улице. В основном в помещении. Хорошо, я понял вас. Вам нужен прибор, черный металл измерять, не отрезая образцы. Подготовку не производить. У нас... Есть сомнения? Нет. Да, но получили мы уже детский металл. И есть сомнения. Ну, допустим, пачка распечатанная. А все листы такой стали. Не дай Бог попадется какой-то в другой сталь. Да, чтобы не было пересортиться. Я понял вас. Мы вам можем предложить мобильный. На колесиках с аргоном. Его можно перевозить в пределах цеха. У него выносной датчик. То есть листы металла не надо отрезать. То есть у вас пришел лист. Просто углерод измерить качественно можно только в среде инертной. Именно в аргоне. Если рассматривать какие-нибудь лазерные. Они более портативные. С достаточно большой погрешностью. То есть, допустим, сталь 20, сталь 40. У него порядок цены 2-2,8 млн. В зависимости от калибровок. Как я понимаю, у вас какие типичные марки? Сталь 20, сталь 3, 0,9, 2С. Мы в Баррексе много используем. Но это уже проблем. Это кругляк. Это в основном низ коллегированных, правильно? Каких-то нержавеек нет? Нержавейка есть? Нержавейка есть. Она не идет на сварный металл конструкции. Мы его на стандартном. У нас есть проблема. Как говорится, сварная металл конструкция. Если где-то попадет центральная сталь. Большое задержание углерода. Запутали на базе. И мы ее варим. Решить вот такую опасность. А если, например, сколько-то лицов пачкать? Какая гарантия? Да, Александр, я понял вашу задачу. У вас, получается, ответственные детали, которые нужно контролировать. Даже 100% на входном контроле. Да. Там и нержавейки. Там у нас и бронза, латунь. Все определяется. То есть вам нужно только одну задачу закрыть. Это черные металлы. Цветные, в принципе, вы можете и на стационаре. Да, да. Вот только черный металл не коллектированный. Чтобы было коллектировано. Хорошо. Может быть, там. Например, сальт. Например, сальт-3. Сальт-35, сальт-40. Сальт-20, сальт-09. Если где-то там кто-то запутает, если нам попадет сальт-45, то обычно металлургия варит какой-то кран большой. Значит, там может попасть. Да, но у вас очень ответственные детали. Мы решим на 100% согласно ГОСТ. Точность будет не хуже, чем ваша стационарная. Как я могу вам коммерческое предложение сделать? Может, сможете мне продиктовать почту или отправить на WhatsApp? Вы предлагаете? Это имеется в виду переносные на колесиках? Вам лазерные, мобильные? Есть просто еще один метод, но там большие погрешности. Сталь, допустим, 30 от стали 40, вы не различите, потому что погрешность высокая. Это к вам не подходит, поэтому я вам даже не предлагаю этот метод. Вам нужно остановиться только на оптико-эмиссионном, но мобильном комплексе. Вот. Да, у вас какой-то бюджет есть? Бюджет-то какой у вас? Бюджет какой у вас? Давайте, Александр, я вам коммерческое предложение выставлю, чтобы вы не с пустыми руками шли к руководству, и отчего вам надо было отталкиваться, потому что в любом случае можно и скидки, и так далее рассмотреть, лизинг там. Давайте. М? Да. Так. Записал. Это придет к вам, да? Александр, хорошо. А у вас какая должность? Ну, начальство следовательского отдела. Ну, хотя бы до соответствующей лицензии будем идти. Хорошо, ну я вам по максимуму информации скину коммерческое предложение. Вот этот номер телефона у вас прямой, да? 6807. Хорошо, хорошо. Все, направим вам. Спасибо. До свидания."
            # },
            # {
            #     "role": "assistant",
            #     "text": "Я должен разделить диалог на покупаетя и на меня, менеджера по продажам. Далее моя задача выделить основные пункты, это может быть, но не обязательно: 1.Как зовут Клиента, в какой компании он работает, какую должность занимает. 2. Задачи которые он преследует. 3.Боль, которую необходимо решить моим продуком. 4.Подробные задачи. 5.Итог, что я должен сделать по завершению общения. Мой ответ должен быть максимально развернутым, не надо придумывать чего не было в разговоре - тебя проверят."
            # },
            # {
            #     "role": "user",
            #     "text": "Начинай выполнять работу, все вводные у тебя есть."
            # }
        ]
    }


    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    apiKey = get_apikey_yandexGPT()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {apiKey}"
    }
    #ajes3cas817lfbgvo9dt
    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    json_data = json.loads(result)
    assistant_text = json_data["result"]["alternatives"][0]["message"]["text"]
    print(result)
    return assistant_text