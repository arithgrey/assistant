from message.models import Message
from conversation.models import Conversation

class MessageService:
    @staticmethod
    def _validate_conversation(conversation):
        if not isinstance(conversation, Conversation):
            raise ValueError("El parámetro 'conversation' debe ser una instancia de Conversation")

    @staticmethod
    def create_user_message(conversation, content):
        MessageService._validate_conversation(conversation)
        return Message.objects.create(
            conversation=conversation,
            content=content,
            is_ia=False
        )

    @staticmethod
    def create_ia_message(conversation, content):
        MessageService._validate_conversation(conversation)
        return Message.objects.create(
            conversation=conversation,
            content=content,
            is_ia=True
        )