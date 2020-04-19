import datetime as dt


def time(request):
    time = dt.datetime.now()
    year = dt.datetime.now().year

    hour = int(time.strftime('%H'))

    if hour >= 12 and hour < 18:
        img_time = ('Day', 'Добрый день!',)
    elif hour >= 18 and hour < 24:
        img_time = ('Evening', 'Добрый вечер!',)
    elif hour >= 0 and hour < 6:
        img_time = ('Night', 'Доброй ночи!',)
    else:
        img_time = ('Morning', 'Доброе утро!',)

    data = {'img_time': img_time, 'time': time, 'year': year,}

    return data
