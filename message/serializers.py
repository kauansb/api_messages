from rest_framework import serializers
from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'direction', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']
