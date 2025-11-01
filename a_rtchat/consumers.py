from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

class ChatroomConsumer(WebsocketConsumer):
  def connect(self):
    self.user = self.scope['user']
    self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name'] 
    self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
    self.accept()   

        
  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    body = text_data_json['body']
    
    message = ChatMessage.objects.create(
        body = body,
        author = self.user, 
        group = self.chatroom 
    )
    context = {
        'message': message,
        'user': self.user,
      #  'chat_group': self.chatroom
    }
    html = render_to_string("a_rtchat/partials/chat_message_p.html", context = context)
    self.send(text_data=html) 
    #     event = {
    #         'type': 'message_handler',
    #         'message_id': message.id,
    #     }
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.chatroom_name, event
    #     )
        
    # def message_handler(self, event):
    #     message_id = event['message_id']
    #     message = GroupMessage.objects.get(id=message_id)
    #     context = {
    #         'message': message,
    #         'user': self.user,
    #         'chat_group': self.chatroom
    #     }
    #     html = render_to_string("a_rtchat/partials/chat_message_p.html", context=context)
    #     self.send(text_data=html)
        
        
    # def update_online_count(self):
    #     online_count = self.chatroom.users_online.count() -1
        
    #     event = {
    #         'type': 'online_count_handler',
    #         'online_count': online_count
    #     }
    #     async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
        
    # def online_count_handler(self, event):
    #     online_count = event['online_count']
        
    #     chat_messages = ChatGroup.objects.get(group_name=self.chatroom_name).chat_messages.all()[:30]
    #     author_ids = set([message.author.id for message in chat_messages])
    #     users = User.objects.filter(id__in=author_ids)
        

