from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

from ..models import CustomUser

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_image', 'birth_date', 'phone_number', 'gender', 'is_active', 'is_online')

    def get_is_online(self, obj):
        if obj.last_online:
            time_difference = timezone.now() - obj.last_online  # Use timezone-aware datetime
            threshold_time = timedelta(seconds=10)
            return time_difference <= threshold_time
        return False


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile_image', 'birth_date', 'phone_number', 'gender')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=False)

class ChangeEmailSerializer(serializers.Serializer):
    old_email = serializers.CharField(required=True)
    new_email = serializers.CharField(required=False)