from django.shortcuts import render
import redis

def index(request):
    r = redis.Redis()
    number = r.get('number')
    if number is None:
        number = 0
        r.set('number', number)
    else:
        number = int(number)
    return render(request, 'index.html', {'number': number})

def next_page(request):
    return render(request, 'next_page.html')
