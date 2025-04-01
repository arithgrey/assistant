import google.generativeai as genai
from django.conf import settings
from conversation.models import Conversation
from assistant.context import AIContext
from cache.services import CacheService
from assistant.tools import Tools

from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType


class AIService:
    def __init__(self, prompt_type: str = None):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash-002")
        self.prompt_type = prompt_type
        self.cache_service = CacheService()
        self.tools = Tools()

    def conversation_history(self, conversation: Conversation) -> str:
        history = []
        for message in conversation.messages.all().order_by('id'):
            role = "[ASISTENTE]" if message.is_ia else "[CLIENTE]"
            history.append(f"{role}: {message.content}")
        return "\n".join(history)


    def generate_response(self, message: str, conversation: Conversation) -> str:
        try:
            context = AIContext.context()
            chat_history_text = self.conversation_history(conversation)

            full_prompt = f"""
            Eres un asistente que puede usar herramientas. 

            {context}
            ESTE ES EL HISTORIAL DE LA CONVERSACIÓN: {chat_history_text} 
            ESTA ES LA NUEVA PREGUNTA DEL CLIENTE: {message}
            """

            # Langchain LLM
            langchain_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-002",
                google_api_key=settings.GOOGLE_API_KEY,
                convert_system_message_to_human=True
            )

            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            agent = initialize_agent(
                tools=self.tools.get_tools(),
                llm=langchain_llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                verbose=True,
                memory=memory
            )

            return agent.run(full_prompt)

        except Exception as e:
            return f"Error generando respuesta con Langchain: {str(e)}"
