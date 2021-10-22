from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field = 'username', 
        read_only = True
    )

    class Meta:
        model = Message
        fields = ["text","created_at", "sender"]