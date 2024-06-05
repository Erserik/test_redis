from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/increment/', consumers.IncrementConsumer.as_asgi()),
]
