from .models import Post, Comment, SavedPost
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer,SavedPostSerializer
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

#Posts CRUDs
#Create posts
class PostCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    ordering_fields=['created_at'] # add the following to show up first

#list of Posts
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    ordering_fields=['created_at'] # add the following to show up first

#fetch a post
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Update posts
class PostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Delete posts
class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Comment Cruds
#Create comments
class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    ordering_fields=['created_at'] # add the following to show up first

#list of comments
class CommentListView(generics.ListAPIView):
    # to get a list of comments that are specific to the post
    def get_queryset(self):
        post_id = self.kwargs['post']
        return Comment.objects.filter(post__id=post_id)
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    ordering_fields=['created_at'] # add the following to show up first

#fetch a comment
class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Update comments
class CommentUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Delete comments
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Like Cruds
#Create Likes


#Read Likes


#Delete Likes

#SavedPost CRUDs
#create SavedPost
class SavedPostCreateView(generics.ListCreateAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    ordering_fields=['created_at']

#List of SavedPosts#####################################################
#Still needs work on the filtering of saved posts to be user specific it currently returning empty list
class SavedPostListView(generics.ListAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user_profile = self.request.user.profile
        print(user_profile)
        return SavedPost.objects.filter(profile=user_profile)
    


#fetch a SavedPost
class SavedPostDetailView(generics.RetrieveAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Delete SavedPosts
class SavedPostDeleteView(generics.DestroyAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]