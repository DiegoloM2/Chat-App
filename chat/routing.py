from django.urls import re_path, path
from chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<room_name>\w+)/$',
     consumers.RoomConsumer.as_asgi()), #regular expression path to 
                                        #serve socket connections to url: 
                                                #ws/chat/<room-name>/\
        path('ws/chat/user/<str:username>/', consumers.ChatConsumer.as_asgi()),
]
