from rest_framework import serializers
from message.models import  Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'is_ia', 'timestamp', 'conversation_id']
  
        
class MessageBotSerializerValidator(serializers.Serializer):    
    
    message = serializers.CharField(            
            required=True,
            min_length=4,
            max_length=200,         
            allow_blank=False,
            error_messages={
                'required': 'Ups! no has enviado una pregunta',
                'min_length': 'La pregunta debe tener al menos 4 caracteres',
                'max_length': '¿Puedes enviar una pregunta más corta?',
                'blank': 'Ups! no has enviado una pregunta'
            }
        )
    
    class Meta:
        required_fields = ["message"]
        not_allow_blank = ["message"]        
        min_lengths = {"message": 4}
        max_lengths = {"message": 200}
        