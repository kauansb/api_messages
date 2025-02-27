import uuid
from django.db import models


class Conversation(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def close(self):
        self.status = 'CLOSED'
        self.save()

    def __str__(self):
        return f"Conversation {self.id} - {self.status}"
