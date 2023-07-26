from rest_framework import serializers

from .models import Chat, Message
from posts.serializers import UserSerializer

# serializers

class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'author_username', 'type', 'text', 'created_at']

class ChatSerializer(serializers.ModelSerializer):
    chat = serializers.SerializerMethodField(method_name='get_chat')
    
    class Meta:
        model = Chat
        fields = ['id', 'chat']
        
    def get_chat(self, obj):
        return f'{obj.user1} - {obj.user2}'

class ChatContactSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    last_message = serializers.SerializerMethodField(method_name='get_last_message')
    
    class Meta:
        model = Chat
        fields = ['id', 'user', 'last_message']
        
    def get_user(self, obj):
        # Get the authenticated user from the context
        authenticated_user = self.context['request'].user

        # Check if the authenticated user is equal to user1 or user2
        if obj.user1 == authenticated_user:
            return UserSerializer(obj.user2).data
        elif obj.user2 == authenticated_user:
            return UserSerializer(obj.user1).data

        return None
    
    def get_last_message(self, obj):
        message = Message.objects.filter(chat=obj).order_by('-created_at').first()
        if message is None:
            return None
        else:
            return MessageSerializer(message).data