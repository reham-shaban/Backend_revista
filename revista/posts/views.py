from django.db.models import Q, Sum
from .models import Post, Comment, Reply, SavedPost,Like
from main.models import Follow, TopicFollow
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, ReplySerializer, SavedPostSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

#Posts CRUDs
#posts [POST, GET]get a list of posts
# Home
class HomePostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile =self.request.user.profile
        queryset = Post.objects.all()
        topics_followed = TopicFollow.objects.filter(profile=profile)
        followings = Follow.objects.filter(follower=profile).values('followed__id')
        queryset = queryset.filter(Q(topics__in=topics_followed.values('topic')) | Q(author__id__in=followings))
        
        # Annotate the queryset with the total points for each post
        queryset = queryset.annotate(
            total_points=Sum('pointed_post__value')
        )
        queryset = queryset.order_by('-total_points')
        return queryset
    
    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile
        serializer.save(author=profile)

#post [GET ,PUT, PATCH, DELETE]
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#Comment Cruds
#list of comments and creating a comment [ GET, POST]
class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def perform_create(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        profile = self.request.user.profile
        content = request.data.get('content')
        comment = Comment.objects.create(post_id=post_id, author=profile, content=content)
        return Response(self.serializer_class(comment).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset=Comment.objects.filter(post__id=post_id)
        return queryset


#comment [GET ,PUT, PATCH, DELETE] get a single comment
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ReplyView(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=ReplySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, request, *args, **kwargs):
        comment_id = self.kwargs['comment_id']
        profile = self.request.user.profile
        content = request.data.get('content')
        reply = Reply.objects.create(comment_id=comment_id, author=profile, content=content)
        return Response(self.serializer_class(reply).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        comment_id=self.kwargs['comment_id']
        queryset=Reply.objects.filter(comment__id=comment_id)
        return queryset

class ReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=ReplySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

#Like Cruds
#Create Likes
class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        profile = self.request.user.profile
        like = Like.objects.create(post_id=post_id, profile=profile)
        return Response(self.serializer_class(like).data, status=status.HTTP_201_CREATED)
    

#Delete Likes
class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#SavedPost CRUDs
#[GET] list saved posts
class SavedPostView(generics.ListAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter queryset to include only saved posts of the authenticated user
        profile = self.request.user.profile
        if profile is not None:
            return SavedPost.objects.filter(profile=profile)
        else:
            return SavedPost.objects.none()
#[POST] save a post
class SavedPostCreateView(generics.CreateAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        profile = self.request.user.profile
        saved = SavedPost.objects.create(post_id=post_id, profile=profile)
        return Response(self.serializer_class(saved).data, status=status.HTTP_201_CREATED)

#[PUT,PATCH,DELETE,GET] get a single saved post
class SavedPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the profile ID and saved_post_id from the URL parameters
        profile = self.request.user.profile
        saved_post_id = self.kwargs['saved_post_id']

        # Retrieve the specific saved post based on the profile ID and saved_post_id
        try:
            saved_post = SavedPost.objects.get(profile=profile, id=saved_post_id)
        except SavedPost.DoesNotExist:
            raise Http404("Saved post does not exist")

        return saved_post

