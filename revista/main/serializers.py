from rest_framework import serializers

from accounts.models import CustomUser
from .models import Profile, Topic, TopicFollow, Follow
from accounts.serializers import UserSerializer

# Profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField(method_name='get_followers_count')
    following_count = serializers.SerializerMethodField(method_name='get_following_count')
   
    class Meta:
        model = Profile
        fields = ('id', 'user', 'cover_image', 'bio', 'followers_count', 'following_count', 'created_at', 'updated_at')
        read_only_fields = ['id', 'user','followers_count', 'following_count', 'created_at', 'updated_at']
          
    def get_followers_count(self, obj):
        followers_count = Follow.objects.filter(followed=obj.id).count()
        return followers_count
    
    def get_following_count(self, obj):
        following_count = Follow.objects.filter(follower=obj.id).count()
        return following_count

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

# Follow
class FollowSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Follow
        fields = ['follower', 'followed']
        read_only_fields = ['follower']

class UserFollowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'profile_image']
        
class ProfileFollowListSerializer(serializers.ModelSerializer):
    user = UserFollowListSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user']
        
class FollowingListSerializer(serializers.ModelSerializer):
    followed = ProfileFollowListSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['followed']
        
class FollowersListSerializer(serializers.ModelSerializer):
    follower = ProfileFollowListSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['follower']