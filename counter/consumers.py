import json
from channels.generic.websocket import WebsocketConsumer
import redis

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

        if action == 'increment':
            r = redis.Redis()
            number = r.incr('number')
            self.broadcast_number(number)
        elif action == 'get':
            r = redis.Redis()
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
        r = redis.Redis()
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
