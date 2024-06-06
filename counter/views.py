from django.shortcuts import render
from django.conf import settings
from redis import Redis

def index(request):
    r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)  # Используйте настройки
    number = r.get('number')
    if number is None:
        number = 0
        r.set('number', number)
    else:
        number = int(number)
    return render(request, 'index.html', {'number': number})

def next_page(request):
    return render(request, 'next_page.html')
