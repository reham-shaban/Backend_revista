from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# Consumers
class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        print(self.user)
        print(self.user.is_authenticated)
        # if not self.user.is_authenticated:
        #     self.close()
        #     return
        
        self.GROUP_NAME = 'user-notifications'
        print(self.GROUP_NAME)
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # if not self.user.is_authenticated:
        async_to_sync(self.channel_layer.group_discard)(
                self.GROUP_NAME, self.channel_name
        )
        
    def user_joined(self, event):
        self.send(text_data=event['text'])
   

# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = 'online'

#         await self.channel_layer.group_add(self.room_name,self.channel_name)

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_name,self.channel_name)


#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         await self.channel_layer.group_send(
#             self.room_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({'message': message}))

