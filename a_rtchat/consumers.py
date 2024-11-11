from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import ChatGroup, GroupMessage
import json
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(self.chatroom_name, self.channel_name)
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        # Creating a message instance in the group
        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )
        
        # Triggering an event to send the message to group members
        event = {
            "type": "message_handler",
            "message_id": message.id
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.chatroom_name, self.channel_name)

    def message_handler(self, event):
        # Fixing key access by adding quotes around "message_id"
        message_id = event["message_id"]
        message = GroupMessage.objects.get(id=message_id)
        
        context = {
            "message": message,
            "user": self.user,
        }
        
        # Rendering HTML for the message
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context=context)
        
        # Sending rendered HTML back to WebSocket
        self.send(text_data=html)
