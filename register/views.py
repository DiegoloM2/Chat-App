from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from friends.models import FriendList
from django.contrib.auth.models import User

def registerView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            FriendList.objects.create(user = user)
            return render(request,"registration/success.html")
        else:
            return render(request, "registration/register.html", {"form": form})

    form = RegisterForm()
    return render(request,"registration/register.html", {"form": form})
