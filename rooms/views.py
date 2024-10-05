from django.shortcuts import render,redirect
from django.core.cache import cache
from cryptography.fernet import Fernet
from django.contrib import messages
import base64
from django.conf import settings
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
cache.clear()
class RoomCache:
    def __init__(self, token):
        self.token = token
        self.cache_key = f"{token}"
        self.cache_key_messages=f"message{token}" 
        self.room_data = {
            "token_of_room": token, 
            "users": [],
        }
    def add_message(self,message):
        messageses = cache.get(self.cache_key_messages,[])
        messageses.append(message)
        cache.set(self.cache_key_messages,messageses)
    @property
    def get_all_message(self):
        messageses= cache.get(self.cache_key_messages,[])
        return messageses

    def set_data(self, **kwargs):
        for key, value in kwargs.items():
            self.room_data[key] = value

        cache.set(self.cache_key, self.room_data, timeout=settings.TIME_OUT)
        cache.set(self.cache_key_messages,[],timeout=settings.TIME_OUT)
    def get_data(self):
        return cache.get(self.cache_key)

    def delete_data(self):
        cache.delete(self.cache_key)
        cache.delete(self.cache_key_messages)

    @staticmethod
    def get_room_data(token):
        cache_key = f"{token}"  
        room_data = cache.get(cache_key) 
        return room_data if room_data else None 
    def add_user(self, username):
        if username not in self.room_data["users"]:
            self.room_data["users"].append(username) 
            cache.set(self.cache_key, self.room_data) 
            return True  
        return False 
    def remove_user(self, username):
        if username in self.room_data["users"]:
            self.room_data["users"].remove(username)  
            cache.set(self.cache_key, self.room_data) 

    def user_exists(self, username):
        """Check if the user exists in the room."""
        return username in self.room_data["users"]
    
key=settings.KEY
def encrypt_message(key, message):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return base64.urlsafe_b64encode(encrypted_message).decode()  # Encode for URL

def decrypt_message(key, encrypted_message):
    f = Fernet(key)
    encrypted_message_bytes = base64.urlsafe_b64decode(encrypted_message.encode())  # Decode from URL
    decrypted_message = f.decrypt(encrypted_message_bytes).decode()
    return decrypted_message

@login_required
@require_POST
def create_room(request):
    data = json.loads(request.body)

    now = datetime.datetime.now()
    expiration_time = now + datetime.timedelta(seconds=settings.TIME_OUT)
    current_user = str(request.user)
    room_cache = RoomCache(key_of_room:=f"{current_user}{int(now.timestamp()*1000000)}")
    room_cache.set_data(users=[],expair=expiration_time, attr="value")
    
    # Get cached rooms for the user, default to an empty list if no cache is found
    y = cache.get(current_user, [])

    # Prepare new cache data with a timestamp one day ahead
    
    new_entry = {key_of_room: expiration_time.timestamp()}

    # Remove any expired entries from the cache (entries with timestamps less than now)
    current_time = datetime.datetime.now().timestamp()
    y = [entry for entry in y if list(entry.values())[0] > current_time]

    # Add the new entry to the cache
    y.append(new_entry)
    cache.set(current_user, y, None)

    return JsonResponse({
        'success': True,
        'room_id':key_of_room,
    })

def Home(request,*kargs,**kwargs):
    
    if request.method == 'POST':
        secret_code = request.POST.get("secretCode")
        room = RoomCache(secret_code)
        room.room_data = room.get_data()

        if room.room_data:
            if request.user.is_authenticated:
                # User is authenticated
                room.add_user(request.user)
                return redirect('Room', room_id=str(encrypt_message(key, secret_code)))
            else:
                # User is not authenticated
                username = request.POST.get("username")

                if request.session.get('username'):
                    room.add_user(request.session['username'])
                    return redirect('Room', room_id=str(encrypt_message(key, secret_code)))
                else:
                    # No username in session, create one
                    request.session['username'] = f"{username}{int(datetime.datetime.now().timestamp() * 1000000)}"
                    room.add_user(request.session['username'])
                    request.session.set_expiry(settings.TIME_OUT)  # Set session expiry to 1 day
                    return redirect('Room', room_id=str(encrypt_message(key, secret_code)))
        else:
            messages.error(request, "Room does not exist or you cannot join.")
    if request.user.is_authenticated:
        y = cache.get(current_user:=str(request.user), [])

        # Prepare new cache data with a timestamp one day ahead

        current_time = datetime.datetime.now().timestamp()
        y = [entry for entry in y if list(entry.values())[0] > current_time]

        # Add the new entry to the cache
        cache.set(current_user, y, None)
        return render(request, "Home.html",{"Rooms":y})
    else:
        return render(request, "Home.html",{})



def Room(request, room_id, *kargs, **kwargs):
    secretcode = decrypt_message(key, room_id)
    room = RoomCache(secretcode)
    room.room_data = room.get_data()

    if room.room_data:
        if request.user.is_authenticated:
            if room.user_exists(request.user):
                return render(request, "room.html",{"secretcode": secretcode,"users":room.room_data["users"],"me":str(request.user)})
            else:
                messages.error(request, "You do not have permission. (403)")
                return redirect("home")  # Adjust to your home URL
        else:
            if room.user_exists(request.session.get('username')):
                return render(request, "room.html", {"secretcode": secretcode,"users":room.room_data["users"],"me":str(request.session.get('username'))})
            else:
                messages.error(request, "You are not logged in or have no permission.")
                return redirect("Home")  # Adjust to your home URL
    else:
        messages.error(request, "Room not found.")
        return redirect("home")  # Adjust to your home URL

