from django.urls import path

from notifications.consumer import NotificationConsumer
from partidas.consumer import PartidaConsumer

websocket_urlpatterns = [
    path("notifications/", NotificationConsumer.as_asgi()),
    path("notifications/partida/", PartidaConsumer.as_asgi()),
]
