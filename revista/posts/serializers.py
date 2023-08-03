from rest_framework import serializers
from .models import Post, Like, Comment,Reply, SavedPost, SearchHistory 
from accounts.models import CustomUser
from main.models import Profile
from main.serializers import TopicSerializer

# Post
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
    like_id= serializers.SerializerMethodField(method_name='get_like')
    saved_post_id= serializers.SerializerMethodField(method_name='get_save')
    topics_details = TopicSerializer(source='topics' ,many=True, read_only=True)
    likes_count = serializers.SerializerMethodField(method_name='get_likes_count')
    comments_count = serializers.SerializerMethodField(method_name='get_comments_count')
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'link', 'topics', 'topics_details', 'image', 'like_id', 'saved_post_id', 'likes_count', 'comments_count', 'created_at', 'updated_at')
    
    def get_like(self, obj):
        request = self.context.get('request', None)   
        print(request)
        user_id = request.user.id
        try:
            like = Like.objects.get(post=obj, profile=user_id)
            return like.id
        except Like.DoesNotExist:
            return 0
        
    def get_save(self, obj):
        request=self.context.get('request', None)
        user_id = request.user.id
        try:
            save = SavedPost.objects.get(post=obj, profile=user_id)
            return save.id
        except SavedPost.DoesNotExist:
            return 0
    
    def get_likes_count(self, obj):
        likes_count = Like.objects.filter(post=obj).count()
        return likes_count
    
    def get_comments_count(self, obj):
        comments_count = Comment.objects.filter(post=obj).count()
        return comments_count


# Like
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'post', 'profile', 'created_at', 'updated_at')

# Comment
class CommentSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    class Meta:
        model= Comment
        fields= ('id', 'post', 'author', 'content',  'created_at', 'updated_at')

# Reply
class ReplySerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    comment=CommentSerializer(read_only=True)
    class Meta:
        model = Reply
        fields = ('id', 'comment', 'author', 'content', 'created_at', 'updated_at')

# Saved Post
class SavedPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    class Meta:
        model = SavedPost
        fields = ('id', 'post', 'profile', 'created_at', 'updated_at')
        
    def get_save(self, obj):
        try:
            save = SavedPost.objects.get(id=obj.id)
            return save.id
        except SavedPost.DoesNotExist:
            return 0
    
    
class SearchHistorySerializer(serializers.ModelSerializer):
    searched_user=UserSerializer(read_only=True)
    class Meta:
        model=SearchHistory
        fields=('id','user','searched_user','search_time','updated_at')
