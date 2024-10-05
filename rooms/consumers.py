from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib import messages
from .views import RoomCache  # Adjust this import based on your project structure

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.username=None
        # Decrypt secret code using the room_id
        self.room = RoomCache(self.room_id)
        self.room.room_data = self.room.get_data()
        print(self.room_id)
        if self.room.room_data:
            user = self.scope['user']
 
            # Check if the user is authenticated or exists in the session
            if user.is_authenticated:
                if self.room.user_exists(user):
                    self.username=str(user)
                    print("Authenticated user exists in room")
                    await self.join_room()
                    msgs=self.room.get_all_message
                    for i in msgs:
                        await self.send(i)
                else:
                    print("Authenticated user does not exist in room")
                    await self.close()
            else:
                # Fallback to session username
                session_username = self.scope['session'].get('username')
                if session_username and self.room.user_exists(session_username):
                    print("Session user exists in room")
                    self.username=str(session_username)
                    await self.join_room()
                    msgs=self.room.get_all_message
                    for i in msgs:
                        await self.send(i)
                else:
                    print("No valid user in session or room")
                    await self.close()
        else:
            # Handle case where room does not exist
            print("Room does not exist")
            await self.close()

    async def join_room(self):
        # Add user to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        message={"type":"remove_user"}
        message["username"]=self.username
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': message["type"],
                'message': message
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message=json.loads(text_data)
        self.send(text_data=json.dumps(message))
        message["username"]=self.username
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': message["type"],
                'message': message
            }
        )
        pass
    async def add_user(self, message):
        self.send()
        await self.send(text_data=json.dumps(message))
    async def remove_user(self,message):
        await self.send(text_data=json.dumps(message))
    async def send_message(self,message):
        await self.send(text_data=json.dumps(message['message']))
        self.room.add_message(json.dumps(message['message']))
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
