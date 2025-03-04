from rest_framework import serializers
from conversation.models import Conversation
from message.serializers import MessageSerializer


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'status', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['id', 'created_at']
        #Pode gerar consultas SQL extras e impactar a performance em grandes volumes de dados.
        #depth = 1  # Mensagens aninhadas automaticamente
