import uuid
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

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

    def handle_new_conversation(self, data):
        conversation_id = data.get("id") or str(uuid.uuid4())
        conversation, created = Conversation.objects.get_or_create(id=conversation_id, defaults={"status": "OPEN"})

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK # Se a conversa já existir, não recriamos
        return Response({"message": "Conversation created.", "id": conversation.id}, status=status_code)

    def handle_new_message(self, data):
        conversation_id = data.get("conversation_id")
        message_id = data.get("id") or str(uuid.uuid4())
        direction = data.get("direction")
        content = data.get("content")
        timestamp = data.get("timestamp")

        if not conversation_id or not content or direction not in ["SENT", "RECEIVED"]:
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
            if parsed_timestamp is None:
                return None  # None explicito para tratar na view
            return parsed_timestamp
        return timezone.now()  # Retorna a hora correta do servidor


class ConversationDetailView(RetrieveAPIView):
    queryset = Conversation.objects.prefetch_related("messages") # Prefetch para evitar N+1(Evita múltiplas queries ao carregar conversas e mensagens associadas.)
    serializer_class = ConversationSerializer
    lookup_field = 'id' # Permitir busca por id


class ConversationListView(ListAPIView):
    queryset = Conversation.objects.prefetch_related("messages")
    serializer_class = ConversationSerializer

    #def get_queryset(self):
    #    return self.queryset.filter(status="OPEN")