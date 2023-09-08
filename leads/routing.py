# leads/routing.py
from django.urls import path
from . import consumer  # make sure you have a consumers.py file in your leads app

websocket_urlpatterns = [
    path('ws/leads/', consumer.LeadsConsumer.as_asgi()),
]
