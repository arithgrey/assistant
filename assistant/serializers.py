# from rest_framework import serializers
# from assistant.models import Conversation
# from message.serializers import MessageSerializer

# class ConversationSerializer(serializers.ModelSerializer):
#     messages = MessageSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Conversation
#         fields = ['id', 'created_at', 'unique_identifier', 'messages']
        
