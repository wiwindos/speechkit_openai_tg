import openai #pip install openai
from config import get_api_key_vsegpt

def text_to_chatGPT35_summarize(text):

    openai.api_key = get_api_key_vsegpt()

    openai.base_url = "https://api.vsegpt.ru/v1/"

    prompt = "нужно произвести сумморизацию текста далее и выделить основные тезисы 1. 2. 3. и тд" + text

    messages = []

    messages.append({"role": "user", "content": prompt})

    response_big = openai.chat.completions.create(
        model="openai/gpt-3.5-turbo-0125",
        messages=messages,
        temperature=0.7,
        n=1,
        max_tokens=int(len(prompt) * 1.5),
        extra_headers={"X-Title": "My App"},  # опционально - передача информация об источнике API-вызова
    )

    # print("Response BIG:",response_big)
    response = response_big.choices[0].message.content
    print("Response:", response)
    return(response)

    """
    # Имя файла для записи списка файлов
    output_file = "summarize.txt"
    
    # Открываем файл для записи
    with open(output_file, "a") as f:
        # Записываем в файл
        f.write(response + "\n")
    """