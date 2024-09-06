from django.shortcuts import render,redirect
from asgiref.sync import sync_to_async
from django.core.cache import cache
from cryptography.fernet import Fernet
from django.contrib import messages
import base64
from django.conf import settings
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
cache.clear()
class RoomCache:
    def __init__(self, token):
        self.token = token
        self.cache_key = f"token{token}"  # Create the key in the desired format
        self.room_data = {
            "token_of_room": token,  # Set default token_of_room value
            "users": [],  # Initialize users as an empty list
        }

    def set_data(self, **kwargs):
        for key, value in kwargs.items():
            self.room_data[key] = value

        # Store data in the cache with a 1-day expiration (86400 seconds)
        cache.set(self.cache_key, self.room_data, timeout=86400)

    def get_data(self):
        return cache.get(self.cache_key)

    def delete_data(self):
        cache.delete(self.cache_key)

    @staticmethod
    def get_room_data(token):
        cache_key = f"token{token}"  # Create the key based on the token
        room_data = cache.get(cache_key)  # Retrieve data from the cache
        return room_data if room_data else None  # Return all attributes or None if not found

    def add_user(self, username):
        if username not in self.room_data["users"]:
            self.room_data["users"].append(username)  # Add user to the list
            cache.set(self.cache_key, self.room_data, timeout=86400)  # Update the cache
            return True  # User was added successfully
        return False  # User already exists
    def remove_user(self, username):
        if username in self.room_data["users"]:
            self.room_data["users"].remove(username)  # Remove user from the list
            cache.set(self.cache_key, self.room_data, timeout=86400)  # Update the cache
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

room_cache = RoomCache("123")

# Set data
room_cache.set_data(token=123, attr="value")

@login_required
@require_POST
def create_room(request):
    data = json.loads(request.body)

    # Cache key with the user and timestamp
    current_user = str(request.user)
    room_cache = RoomCache(key_of_room:=f"{current_user}{int(datetime.datetime.now().timestamp()*1000000)}")
    room_cache.set_data(users=[], attr="value")
    
    # Get cached rooms for the user, default to an empty list if no cache is found
    y = cache.get(current_user, [])

    # Prepare new cache data with a timestamp one day ahead
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
    new_entry = {key_of_room: expiration_time.timestamp()}

    # Remove any expired entries from the cache (entries with timestamps less than now)
    current_time = datetime.datetime.now().timestamp()
    y = [entry for entry in y if list(entry.values())[0] > current_time]

    # Add the new entry to the cache
    y.append(new_entry)
    cache.set(current_user, y, None)

    return JsonResponse({
        'success': True,
        'room_id': 2323,
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
                    request.session.set_expiry(86400)  # Set session expiry to 1 day
                    return redirect('Room', room_id=str(encrypt_message(key, secret_code)))
        else:
            messages.error(request, "Room does not exist or you cannot join.")
    if request.user.is_authenticated:
        y = cache.get(current_user:=str(request.user), [])

        # Prepare new cache data with a timestamp one day ahead
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)

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

