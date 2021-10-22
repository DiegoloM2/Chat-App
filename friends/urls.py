from django.urls import path
from . import views
urlpatterns = [
    path('', views.FriendView.as_view(), name = "friends"), 
    path('declineFriendRequest/<int:pk> ', views.declineFriendRequest,name = "declineFriendRequest"),
    path('acceptFriendRequest/<int:pk> ', views.acceptFriendRequest,name = "acceptFriendRequest"),
    path('cancelFriendRequest/<int:pk> ', views.declineFriendRequest,name = "cancelFriendRequest"),
]