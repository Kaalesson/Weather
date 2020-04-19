import os

from dotenv import load_dotenv
import requests
from django.shortcuts import render

from .forms import Cityform

load_dotenv()


URL = 'https://api.openweathermap.org/data/2.5/weather/'
PROXI = {'https': '144.217.101.242:3129'}
TOKEN = os.getenv('TOKEN')


def index(request):
    form = Cityform()
    return render(request, 'index.html', {'form': form})


def weather_day(request):
    form = Cityform(request.POST or None)
    if form.is_valid():
        cityname = form.cleaned_data.get("city_name")

    params = {
        'q': f'{cityname}',
        'units': 'metric',
        'lang': 'ru',
        'appid': f'{TOKEN}',
    }

    try:
        weather_params = requests.post(
            url=URL,
            params=params, proxies=PROXI).json()

    except requests.RequestException:
        print('Ошибка при получении данных')
        return render(request, '404.html')

    if weather_params['cod'] == 200:
        condition = weather_params['weather'][0]['description']
        pressure = int(weather_params['main']['pressure'] * 0.750062)

        vars = {
            'cod': weather_params['cod'],
            'pressure': pressure,
            'condition': condition,
            'cityname': cityname,
            'weather': weather_params['weather'],
            'main': weather_params['main'],
            'wind': weather_params['wind'],
        }
        return render(request, 'weather.html', {'vars': vars})

    else:
        vars = {
            'cod': weather_params['cod'],
            'cityname': cityname,
        }
        return render(request, 'weather.html', {'vars': vars})
