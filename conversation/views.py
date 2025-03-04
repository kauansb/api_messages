from datetime import datetime
import uuid
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import Conversation
from message.models import Message
from .serializers import ConversationSerializer


class WebhookView(APIView):

    def post(self, request):
        event_type = request.data.get("type")
        data = request.data.get("data", {})

        if event_type == "NEW_CONVERSATION":
            return self.handle_new_conversation(data)

        elif event_type == "NEW_MESSAGE":
            return self.handle_new_message(data)

        elif event_type == "CLOSE_CONVERSATION":
            return self.handle_close_conversation(data)

        return Response({"error": "Invalid event type."}, status=status.HTTP_400_BAD_REQUEST)

    def handle_new_conversation(self, data):
        conversation_id = data.get("id") or str(uuid.uuid4())
        conversation, created = Conversation.objects.get_or_create(id=conversation_id)
        return Response({"message": "Conversation created.", "id": conversation.id}, status=status.HTTP_201_CREATED)

    def handle_new_message(self, data):
        conversation_id = data.get("conversation_id")
        message_id = data.get("id") or str(uuid.uuid4())
        direction = data.get("direction")
        content = data.get("content")
        timestamp = data.get("timestamp")

        if not conversation_id or not content:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, id=conversation_id)

        if conversation.status == "CLOSED":
            return Response(
                {"error": "Cannot add messages to a closed conversation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Garante um timestamp válido
        timestamp_parsed = self.validate_timestamp(timestamp)
        if timestamp_parsed is None:
            return Response({"error": "Invalid timestamp format."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            id=message_id,
            conversation=conversation,
            direction=direction,
            content=content,
            timestamp=timestamp_parsed
        )

        return Response({"message": "Message created."}, status=status.HTTP_201_CREATED)

    def handle_close_conversation(self, data):
        conversation = get_object_or_404(Conversation, id=data.get("id"))
        conversation.close()
        return Response({"message": "Conversation closed."}, status=status.HTTP_200_OK)

    def validate_timestamp(self, timestamp):
        if isinstance(timestamp, str):
            parsed_timestamp = parse_datetime(timestamp)
            return parsed_timestamp if parsed_timestamp else None
        return datetime.now()


class ConversationDetailView(APIView):

    def get(self, request, id):
        try:
            conversation = get_object_or_404(Conversation, id=id)
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversationListView(ListAPIView):
    """Lista todas as conversas"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer