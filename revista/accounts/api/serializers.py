from rest_framework import serializers
from ..models import CustomUser

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_image', 'birth_date', 'phone_number', 'gender','is_active')

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