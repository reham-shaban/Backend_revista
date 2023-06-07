from rest_framework import serializers
from .models import Post, Comment,SavedPost

class PostSerializer(serializers.ModelSerializer):
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