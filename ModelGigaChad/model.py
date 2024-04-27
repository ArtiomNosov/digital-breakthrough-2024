# Используем вкладку "Секреты" левой панели Colab для хранения ключей
# from google.colab import userdata
client_id = '381eb810-6196-4603-98f0-65e3a26849fb'# userdata.get('SBER_ID')
secret = '09ba618f-4932-4e66-8de7-dc81a072f323' # userdata.get('SBER_SECRET')
auth = 'MzgxZWI4MTAtNjE5Ni00NjAzLTk4ZjAtNjVlM2EyNjg0OWZiOjA5YmE2MThmLTQ5MzItNGU2Ni04ZGU3LWRjODFhMDcyZjMyMw==' # userdata.get('SBER_AUTH')

import base64
credentials = f"{client_id}:{secret}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

import requests
import uuid

def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.

      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - область (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».

      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

response = get_token(auth)
if response != 1:
  print(response.text)
  giga_token = response.json()['access_token']

import requests
import json

def get_chat_completion(auth_token, user_message):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.

    Параметры:
    - auth_token (str): Токен для авторизации в API.
    - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.

    Возвращает:
    - str: Ответ от API в виде текстовой строки.
    """
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": user_message  # Содержание сообщения
            }
        ],
        "temperature": 1,  # Температура генерации
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 512,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1

# prompt_time = '''
# Из текста ниже тебе необходимо понять на сколько дней идёт сдвиг относительно текущего врмени в днях
# Если речь идёт о будущем, то число положительное
# Если речь идёт о прошлом, то число отрицательное
# Примеры
# 1. Текст: две недели назад. Ответ: -14
#
# Текст: через месяц
# '''
#
# answer = get_chat_completion(giga_token, prompt_time)
#
# answer.json()
#
# print(answer.json()['choices'][0]['message']['content'])
#
# from IPython.display import display, Markdown
# display(Markdown(answer.json()['choices'][0]['message']['content']))