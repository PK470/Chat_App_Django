import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from core.models import Message
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user1 = self.scope['user'].email  # Use email for the authenticated user
        user2 = self.room_name  # The room name should be the receiver's email

        # Sanitize group name to ensure it's valid
        sorted_users = ''.join(sorted([user1, user2]))
        sanitized_group_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", sorted_users)
        self.room_group_name = f"chat_{sanitized_group_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']  # Sender is the currently authenticated user
        receiver = await self.get_receiver_user()

        if receiver is None:
            # Handle case where receiver doesn't exist
            await self.send(text_data=json.dumps({'error': 'Receiver does not exist'}))
            return

        await self.save_message(sender, receiver, message)

        # Send message to WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender.email,  # Use email as identifier for the sender
                'receiver': receiver.email,  # Use email as identifier for the receiver
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'receiver': receiver,
            'message': message
        }))

    @sync_to_async
    def save_message(self, sender, receiver, message):
        Message.objects.create(sender=sender, receiver=receiver, content=message)

    @sync_to_async
    def get_receiver_user(self):
        try:
            User = get_user_model()
            
            return User.objects.get(email=self.room_name)
        except User.DoesNotExist:
            return None
