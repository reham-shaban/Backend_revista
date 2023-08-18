from rest_framework import serializers

from .models import Live
from accounts.api.serializers import UserSerializer

# serializers
class LiveSerializer(serializers.ModelSerializer):
    streamer = UserSerializer(read_only=True)
    class Meta:
        model = Live
        fields = ['id', 'streamer', 'title', 'description', 'created_at']
        read_only_fields = ['streamer']
        
    def create(self, validated_data):
        user = self.context['request'].user    
        live = Live.objects.create(**validated_data, streamer=user)
        return live