from rest_framework import serializers
from .models import Conversation, ChatRoom


class ConversationSerializer(serializers.ModelSerializer):
    class Meta():
        model = Conversation
        fields = '__all__'
    
    def create(self, validated_data):
        conversation = Conversation.objects.create(
            prompt = validated_data['prompt'],
            response = validated_data['response'],
        )
        
        return conversation


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta():
        model = ChatRoom
        fields = '__all__'
    
    def create(self, validated_data):
        return ChatRoom(**validated_data)