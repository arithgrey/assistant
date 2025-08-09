import google.generativeai as genai
from django.conf import settings
from conversation.models import Conversation
from assistant.context import AIContext
from cache.services import CacheService
from langchain.tools import Tool
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.google import GoogleGenerativeAI

class AIService:
    def __init__(self, prompt_type: str = None):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.llm = GoogleGenerativeAI(model="gemini-1.5-flash-002", google_api_key=settings.GOOGLE_API_KEY)
        self.prompt_type = prompt_type
        self.cache_service = CacheService()
        self.tools = self._initialize_tools()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = self._initialize_agent()

    def _initialize_tools(self) -> list:
        tools = [
            Tool(
                name="BuscarProductos",
                func=self.cache_service.products_category,
                description="Útil para buscar productos por categoría en el catálogo"
            ),
            Tool(
                name="ProductosMasVendidos",
                func=self.cache_service.top_sellers,
                description="Obtiene la lista de productos más vendidos"
            )
        ]
        return tools

    def _initialize_agent(self):
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )

    def conversation_history(self, conversation: Conversation) -> str:
    
        history = []
        for message in conversation.messages.all().order_by('id'):
            role = "[ASISTENTE]" if message.is_ia else "[CLIENTE]"
            history.append(f"{role}: {message.content}")
        
        return "\n".join(history)

    def generate_response(self, message: str, conversation: Conversation) -> str:
        try:
            chat_history = self.conversation_history(conversation)
            self.memory.chat_memory.add_user_message(chat_history)
            
            context = AIContext.context(
                top_sellers=self.cache_service.top_sellers(), 
                accesorios=self.cache_service.products_category()
            )
            
            full_message = f"""
            {context}
            ESTE ES EL HISTORIAL DE LA CONVERSACIÓN: {chat_history} 
            ESTA ES LA NUEVA PREGUNTA DEL CLIENTE: {message}
            """
            
            response = self.agent.run(full_message)
            return response if response else "Lo siento, no pude procesar tu mensaje."
        except Exception as e:
            return f"Error generando respuesta: {str(e)}"
        
    