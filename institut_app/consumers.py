
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            print(f"DEBUG WS: Connection accepted for user {self.user.username} in group {self.group_name}")

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        message = event['message']
        link = event.get('link')
        notif_id = event.get('id')
        extra_data = event.get('extra_data')
        print(f"DEBUG WS: Sending message to user {self.user.id}: {message}")
        await self.send(text_data=json.dumps({
            'message': message,
            'link': link,
            'id': notif_id,
            'extra_data': extra_data
        }))
