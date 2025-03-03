from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Conversation


class ConversationTests(APITestCase):
    def test_create_conversation(self):
        url = reverse('conversation-list-create')
        data = {'status': 'OPEN'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)