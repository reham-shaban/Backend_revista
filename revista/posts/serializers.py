from rest_framework import serializers
from .models import Post, Comment,SavedPost,Like
from accounts.models import CustomUser
from main.models import Profile
from main.serializers import TopicSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields=('id','username','profile_image','first_name', 'last_name')
        
class AuthorSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model= Profile
        fields=('id','user')
        
        
class PostSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    topics=TopicSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'link', 'topics', 'image', 'likes_count', 'comments_count', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields= ('id', 'post', 'author', 'content', 'created_at', 'updated_at')

class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = ('id','post', 'profile', 'created_at', 'updated_at')
        


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id','post', 'profile', 'created_at', 'updated_at')
