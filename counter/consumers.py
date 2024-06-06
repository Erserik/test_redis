import json
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from redis import Redis

class IncrementConsumer(WebsocketConsumer):
    clients = []

    def connect(self):
        self.accept()
        IncrementConsumer.clients.append(self)
        self.send_number()

    def disconnect(self, close_code):
        IncrementConsumer.clients.remove(self)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)  # Используйте настройки

        if action == 'increment':
            number = r.incr('number')
            self.broadcast_number(number)
        elif action == 'get':
            number = r.get('number')
            if number is None:
                number = 0
                r.set('number', number)
            else:
                number = int(number)
            self.send(text_data=json.dumps({
                'number': number
            }))

    def send_number(self):
        r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)  # Используйте настройки
        number = r.get('number')
        if number is None:
            number = 0
            r.set('number', number)
        else:
            number = int(number)
        self.send(text_data=json.dumps({
            'number': number
        }))

    @classmethod
    def broadcast_number(cls, number):
        for client in cls.clients:
            client.send(text_data=json.dumps({
                'number': number
            }))
