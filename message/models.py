import uuid
from django.db import models
from conversation.models import Conversation


class Message(models.Model):
    MESSAGE_TYPES = [
        ('SENT', 'Sent'),
        ('RECEIVED', 'Received'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    direction = models.CharField(max_length=8, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Message {self.id} ({self.direction})"