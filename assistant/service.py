import google.generativeai as genai
from django.conf import settings
from conversation.models import Conversation
from assistant.context import AIContext
from cache.services import CacheService

class AIService:
    def __init__(self, prompt_type: str = None):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash-002")
        self.prompt_type = prompt_type
        self.cache_service = CacheService()


    def conversation_history(self, conversation: Conversation) -> str:
    
        history = []
        for message in conversation.messages.all().order_by('id'):
            role = "[ASISTENTE]" if message.is_ia else "[CLIENTE]"
            history.append(f"{role}: {message.content}")
        
        return "\n".join(history)

    def generate_response(self, message: str, conversation: Conversation) -> str:
        try:
            top_sellers = self.cache_service.top_sellers()
            accesorios = self.cache_service.products_category()

            context = AIContext.context(top_sellers=top_sellers, accesorios=accesorios)
            chat_history = self.conversation_history(conversation)
            
            
            full_message = f"""
            {context}
            ESTE ES EL HISTORIAL DE LA CONVERSACIÓN: {chat_history} 
            ESTA ES LA NUEVA PREGUNTA DEL CLIENTE: {message}
            """
            
            response = self.model.generate_content(full_message)
            return response.text if response else "Lo siento, no pude procesar tu mensaje."
        except Exception as e:
            return f"Error generando respuesta: {str(e)}"
        
    