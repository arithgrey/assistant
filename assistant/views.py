from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from conversation.models import Conversation
from conversation.serializers import ConversationSerializer
from message.serializers import MessageBotSerializerValidator
from assistant.service import AIService
from message.service import MessageService
from conversation.service import ConversationService
from cache.services import CacheService

class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai_service = AIService(prompt_type="customer_service")
        self.cache_service = CacheService()
    
    @action(detail=False, methods=['POST'], url_path='send-message')
    def send_message(self, request):
        conversation_id = request.data.get('conversation_id')
        
        serializer = MessageBotSerializerValidator(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        
        # Obtener top_sellers antes de generar la respuesta
        top_sellers = self.cache_service.top_sellers()
        accesorios = self.cache_service.products_category()
        
        user_message = serializer.validated_data['message']
        conversation = ConversationService.get_or_create_conversation(conversation_id)
        user_message = MessageService.create_user_message(conversation, user_message)
        response = self.ai_service.generate_response(
            message=user_message, 
            conversation=conversation, 
            top_sellers=top_sellers,
            accesorios=accesorios)
        
        ia_message = MessageService.create_ia_message(conversation, response)

        return Response({
            'conversation_id': conversation.id,
            'status': 'success',
            'conversation': {
                'id': conversation.id,
                'unique_identifier': str(conversation.unique_identifier)
            },
            'user_message': {
                'message_id': user_message.id,
                'content': user_message.content
            },
            'ai_response': {
                'message_id': ia_message.id,
                'content': ia_message.content
            }
        }, status=status.HTTP_201_CREATED)
   