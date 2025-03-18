from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from conversation.models import Conversation
from conversation.serializers import ConversationSerializer
from message.serializers import MessageBotSerializerValidator
from assistant.service import AIService
from message.service import MessageService
from conversation.service import ConversationService
import requests

class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai_service = AIService(prompt_type="customer_service")
        
    
    @action(detail=False, methods=['POST'], url_path='send-message')
    def send_message(self, request):
        conversation_id = request.data.get('conversation_id')
        
        serializer = MessageBotSerializerValidator(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        
        # Obtener top_sellers antes de generar la respuesta
        top_sellers_response = self.get_top_sellers()
        top_sellers_data = top_sellers_response.data if top_sellers_response.status_code == 200 else None
        user_message = serializer.validated_data['message']
        conversation = ConversationService.get_or_create_conversation(conversation_id)
        user_message = MessageService.create_user_message(conversation, user_message)
        response = self.ai_service.generate_response(user_message, conversation, top_sellers_data)
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
    
    def get_top_sellers(self):
        try:
            url = 'https://enidservice.com/api/enid/productos/top-sellers/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
                'Accept': 'application/json, text/plain, */*',
                'X-Store-Id': '1',
                'Referer': 'https://enidservice.com/'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return Response(response.json(), status=status.HTTP_200_OK)
            
        except requests.RequestException as e:
            return Response(
                {'error': 'Error al obtener los productos', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
  