from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync

from accounts.models import CustomUser
import re, json

from .models import Notification

# Consumers
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):        
        # get id from headers
        id_string = self.scope['headers'][6][1]
        s = id_string.decode('utf-8')
        match = re.search(r'\d+',s)
        id = int(match.group())
        print(id)
        
        # get the user object
        self.user = await sync_to_async(CustomUser.objects.filter(id=id).first)()
        print(self.user)
      
        if self.user:
            self.GROUP_NAME = f'user-notifications-{id}'
            
            print(self.GROUP_NAME)

            # Add the consumer to the user notifications group
            await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)

            # Accept the WebSocket connection
            await self.accept()
            
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Remove the consumer from the user notifications group
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

    async def follow_notification(self, event):
        print('In follow_notification')
         
        follower_username = event['text']['username']
        follower_profile_image = event['text']['profile_image']
        detail = event['text']['detail']
        created_at = event['text']['created_at']
         
        # # Create a new Notification object
        # notification = Notification.objects.create(
        #     user= self.user,
        #     type='Follow',
        #     image=follower_profile_image,
        #     detail=f'{follower_username} started following you.',
        # )
        
        # # Save the notification to the database
        # notification.save()
        
         
        data = {
            'username': follower_username,
            'profile_image': follower_profile_image,
            'detail': detail,
            'created_at': created_at,
        }
        
        await self.send(text_data=f'{follower_username} started following you.')
        
  

# the one we tested
# class NotificationConsumer(WebsocketConsumer):
#     def connect(self):
#         self.user = self.scope['user']
#         self.GROUP_NAME = 'user-notifications'
        
#         async_to_sync(self.channel_layer.group_add)(
#             self.GROUP_NAME, self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#                 self.GROUP_NAME, self.channel_name
#         )
        
#     def user_joined(self, event):
#         self.send(text_data=event['text'])
   

# for message

# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'online'

        await self.channel_layer.group_add(self.room_name,self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name,self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))