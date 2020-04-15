import os
import datetime as dt

from dotenv import load_dotenv
import requests

from django.shortcuts import render

load_dotenv()


TIME = time = dt.datetime.now()
URL = 'https://api.weather.yandex.ru/v1/forecast/'
YANDEX_WEATHER_TOKEN = os.getenv('YANDEX_WEATHER_TOKEN')
CONDITION_DATA = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',   
    'overcast': 'пасмурно',
    'partly-cloudy-and-light-rain': 'небольшой дождь',
    'partly-cloudy-and-rain': 'дождь',
    'overcast-and-rain': 'сильный дождь',
    'overcast-thunderstorms-with-rain': 'сильный дождь, гроза',
    'cloudy-and-light-rain': 'небольшой дождь',
    'overcast-and-light-rain': 'небольшой дождь',
    'cloudy-and-rain': 'дождь',
    'overcast-and-wet-snow': 'дождь со снегом',
    'partly-cloudy-and-light-snow': 'небольшой снег',
    'partly-cloudy-and-snow': 'снег',
    'overcast-and-snow': 'снегопад',
    'cloudy-and-light-snow': 'небольшой снег',
    'overcast-and-light-snow': 'небольшой снег',
    'cloudy-and-snow': 'снег',
}


def index(request):
    hour = int(TIME.strftime('%H'))
    if hour >= 12 and hour < 18:
        info = 'Добрый день!'
    elif hour > 18 and hour < 24:
        info = 'Добрый вечер!'
    elif hour >= 0 and hour < 6:
        info = 'Доброй ночи!'
    else:
        info = 'Добре утро!'
    return render(request, 'index.html', {'info': info})


def weather_day(request):
    headers = {'X-Yandex-API-Key': f'{YANDEX_WEATHER_TOKEN}'}
    params = {}

    try:
        weather_params_all = requests.get(
            url=URL,
            params=params,
            headers=headers).json()

        weather_params = weather_params_all['fact']
        condition = CONDITION_DATA[weather_params['condition']]

        return render(request, 'weather.html', {
            'temp': weather_params['temp'],
            'feels_like': weather_params['feels_like'],
            'weather_condition': condition,
            'wind_speed': weather_params['wind_speed'],
            'pressure': weather_params['pressure_mm'],
            'humidity': weather_params['humidity'],
        })

    except requests.HTTPError as err:
        code = err.response.status_code
        print(f'Ошибка, status code: {code}')
        return {}

    except requests.RequestException:
        print('Ошибка при получении данных')
        return {}