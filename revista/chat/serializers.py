from rest_framework import serializers

from .models import Chat, Message
from posts.serializers import UserSerializer

# serializers

# Used in chat contact for last message
class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'author_username', 'type', 'text', 'created_at']
    
class ChatSerializer(serializers.ModelSerializer):
    chat = serializers.SerializerMethodField(method_name='get_chat')
    messages_count = serializers.SerializerMethodField(method_name='get_messages_count')
    
    class Meta:
        model = Chat
        fields = ['id', 'chat', 'messages_count']
        
    def get_chat(self, obj):
        return f'{obj.user1} - {obj.user2}'
    
    def get_messages_count(self, obj):
        messages_count = Message.objects.filter(chat=obj).count()
        return messages_count

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
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_data = data.get('user', None)
        
        if user_data and user_data['profile_image']:
            # Get the request object from the context
            request = self.context.get('request', None)

            # Generate the absolute URL for the profile_image field
            profile_image_url = request.build_absolute_uri(user_data['profile_image'])
            user_data['profile_image'] = profile_image_url

        return data