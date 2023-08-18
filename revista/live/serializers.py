from rest_framework import serializers

from .models import Live

# serializers
class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = ['id', 'streamer', 'title', 'description', 'created_at']
        read_only_fields = ['streamer']
        
    def create(self, validated_data):
        user = self.context['request'].user    
        live = Live.objects.create(**validated_data, streamer=user)
        return live