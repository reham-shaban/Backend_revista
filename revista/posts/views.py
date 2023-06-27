from .models import Post, Comment, SavedPost,Like
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer,SavedPostSerializer,LikeSerializer
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from django.http import Http404

#Posts CRUDs
#posts [POST, GET]get a list of posts
class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    ordering_fields=['created_at'] # add the following to show up first
    def get_queryset(self):
        queryset = Post.objects.all()
        topic_ids = self.request.query_params.getlist('topic_id')
        queryset = queryset.filter(topics__id__in=topic_ids)
        return queryset

#post [GET ,PUT, PATCH, DELETE]
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Comment Cruds
#list of comments and creating a comment [ GET, POST]
class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    ordering_fields=['created_at'] # add the following to show up first

#comment [GET ,PUT, PATCH, DELETE] get a single comment
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Like Cruds
#Create Likes
class LikeCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Delete Likes
class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#SavedPost CRUDs
class SavedPostListCreateView(generics.ListCreateAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    ordering_fields=['created_at']
    def get_queryset(self):
        # Filter queryset to include only saved posts of the authenticated user
        profile = self.request.data.get('profile')
        if profile is not None:
            return SavedPost.objects.filter(profile__id=profile)
        else:
            return SavedPost.objects.none()

class SavedPostDetailView(generics.RetrieveDestroyAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the profile ID and post ID from the URL parameters
        profile_id = self.kwargs['profile_id']
        post_id = self.kwargs['post_id']

        # Retrieve the specific saved post based on the profile ID and post ID
        try:
            saved_post = SavedPost.objects.get(profile__id=profile_id, post__id=post_id)
        except SavedPost.DoesNotExist:
            raise Http404("Saved post does not exist")

        return saved_post

