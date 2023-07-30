from rest_framework import serializers

from .models import Notification

# serializers
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['type', 'forward_id', 'profile_image', 'detail', 'created_at']