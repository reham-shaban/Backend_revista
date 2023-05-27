from rest_framework import serializers

from .models import Profile, Topic, TopicFollow
from accounts.serializers import UserSerializer

# Profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'cover_image', 'bio', 'followers_count', 'following_count', 'created_at', 'updated_at')
        read_only_fields = ['id', 'user','followers_count', 'following_count', 'created_at', 'updated_at']

# Topic
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'image']
        
# Topic Follow
class TopicFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicFollow
        fields = ['id', 'profile', 'topic']
        read_only_fields = ['profile']
