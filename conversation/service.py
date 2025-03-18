from conversation.models import Conversation
from rest_framework import serializers

class ConversationService:
    @staticmethod
    def get_or_create_conversation(conversation_id=None):
        """
        Valida y obtiene una conversación existente o crea una nueva
        """
        if not conversation_id:
            return Conversation.objects.create()
        
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError(
                {'error': f'Conversación {conversation_id} no encontrada'}
            )