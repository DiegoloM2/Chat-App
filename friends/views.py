from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse    
from django.views import View
from .models import FriendRequest, FriendList
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
import json
# Create your views here.
User = get_user_model()
class FriendView(View, LoginRequiredMixin):
    def get(self, request):
        user = request.user
        friendList = FriendList.objects.get(user = user)
        print(friendList.friends.all())

        receivedFriendRequests = FriendRequest.objects.filter(receiver = user, is_active = True)
        sentFriendRequests = FriendRequest.objects.filter(sender = user, is_active = True)

        return render(request, "friends.html", {
            "friendList":friendList.friends.all(),
            "receivedFriendRequests":receivedFriendRequests,
            "sentFriendRequests":sentFriendRequests 
        })


    def post(self, request):
        try: 
            receiver = User.objects.get(username = request.POST.get('receiver'))
            FriendRequest.objects.create(sender = request.user, receiver = receiver) 
            return JsonResponse({}, status = 201)
        except User.DoesNotExist:
            return JsonResponse({}, status = 404)


def acceptFriendRequest(request, pk):
    friendRequest = get_object_or_404(FriendRequest, pk = pk)
    friendRequest.accept()
    
    return JsonResponse({}, status = 201)

def declineFriendRequest(request, pk):
    friendRequest = get_object_or_404(FriendRequest, pk = pk)
    request
    friendRequest.decline()
    return JsonResponse({}, status = 200)

def cancelFriendRequest(request, pk):
    friendRequest = get_object_or_404(FriendRequest, pk = pk)
    friendRequest.cancel()
    return JsonResponse({}, status= 200)