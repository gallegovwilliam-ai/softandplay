from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class PartidaConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            self.close(code=4401)
            return
        self.group_name = 'partida'
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        # El navegador no debe poder disparar eventos de partida para todos.
        # Los eventos se generan exclusivamente desde el servidor.
        user = self.scope.get("user")
        if not user or user.is_anonymous or not user.is_superuser:
            return
        try:
            json.loads(text_data or '{}')
        except (TypeError, ValueError):
            return
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {"type": "notify", "text": {"reload": "SI"}},
        )

    def notify(self, event):
        self.send(text_data=json.dumps(event["text"]))
