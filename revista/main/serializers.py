from rest_framework import serializers
import base64
from django.core.files.storage import default_storage

from .models import Topic, TopicFollow

# Topic
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'image']
        
# Topic Follow
class TopicFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicFollow
        fields = ['id', 'user', 'topic']
        read_only_fields = ['user'] 

    def create(self, validated_data):
        user = self.context['request'].user  # Get the authenticated user
        validated_data['user'] = user  # Assign the user to the validated data
        return super().create(validated_data)
    
