from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from friends.models import FriendList
from .models import Thread, Message
from .serializers import MessageSerializer

def index(request): 
    return render(request, "chat/index.html")

@login_required #make login required
def room(request, room_name): 
    return render(request, "chat/room.html", {
        "room_name": mark_safe(json.dumps(room_name)), 
        "username": mark_safe(json.dumps(request.user.username))
    })

# @login_required
# def privateChat(request, username):
#     receiver = User.objects.get(username = username)

#     sender = request.user

#     friendList = FriendList.objects.get(user = sender)

#     thread_obj = Thread.objects.get_or_create_personal_thread(user1 = sender, user2 = receiver)

#     messages = Message.last_15_messages(thread = thread_obj)
    
#     friends = Message.orderUsersByMessages(friendList.friends.all())
#     friends = [friend[0] for friend in friends.values_list('username')]

#     return render(request, "chat/privateChat.html", {
#         "sender": sender.username,
#         "receiver":receiver.username, 
#         "friends": friends, 
#         "messages": messages

#     })


@login_required

def privateChat(request):
    sender = request.user

    friendList = FriendList.objects.get(user = sender)

    friends = Message.orderUsersByMessages(friendList.friends.all())
    receiver = friends.first()

    friends = [friend[0] for friend in friends.values_list('username')]


    thread_obj = Thread.objects.get_or_create_personal_thread(sender, receiver)
    
    messages = Message.last_15_messages(thread = thread_obj)

    return render(request, "chat/privateChat.html", {
        "sender":sender.username, 
        "receiver": receiver.username, 
        "friends":friends, 
        "messages":messages
    })

@login_required
def get_private_msgs(request, username):
    sender = request.user
    receiver = User.objects.get(username = username)

    thread_obj = Thread.objects.get_or_create_personal_thread(sender, receiver)

    messages = Message.last_15_messages(thread = thread_obj)
    messages = MessageSerializer(messages, many = True)

    return JsonResponse({
        "sender":sender.username, 
        "receiver":receiver.username,
        "messages":messages.data
    }, status = 200)
