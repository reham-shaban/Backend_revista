from django.db.models import Q, Sum
from django.db import IntegrityError
from .models import Post, Comment, Reply, SavedPost,Like,SearchHistory
from main.models import Follow, TopicFollow, Block
from accounts.models import CustomUser
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, ReplySerializer, SavedPostSerializer, LikeSerializer, UserSerializer, SearchHistorySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from knox.auth import TokenAuthentication
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CustomUserFilter



# Post 
# [POST]: create post, [GET]: posts list in home
class HomePostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile =self.request.user.profile
        queryset = Post.objects.all()
        topics_followed = TopicFollow.objects.filter(profile=profile)
        followings = Follow.objects.filter(follower=profile).values('followed__id')
        # filter queryset based on topics & users followed
        queryset = queryset.filter(Q(topics__in=topics_followed.values('topic')) | Q(author__id__in=followings))
        
        # Annotate the queryset with the total points for each post
        queryset = queryset.annotate(
            total_points=Sum('pointed_post__value')
        )
        # order queryset based on points
        queryset = queryset.order_by('-total_points', '-created_at')
        return queryset
    
    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile
        serializer.save(author=profile)
        
# single post [GET ,PUT, PATCH, DELETE]
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# admin get all posts
class PostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
# my profile posts
class MyTimeLineView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile =self.request.user.profile
        queryset = Post.objects.all()
        querset=queryset.filter(author=profile)
        return querset
    
# vistor profile posts
class TimeLineView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = Post.objects.all()
        querset = queryset.filter(author_id=profile_id)
        return querset

# Discover Page
class DiscoverView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        topic_id = self.kwargs.get('topic_id')
        queryset = Post.objects.all()
        if topic_id != 0:
            queryset=queryset.filter(topics__id=topic_id)
        queryset = queryset.annotate(total_points=Sum('pointed_post__value'))
        queryset = queryset.order_by('-total_points', '-created_at')
        return queryset

class GeneralView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Post.objects.all()
        queryset = queryset.annotate(total_points=Sum('pointed_post__value'))
        queryset = queryset.order_by('-total_points','-created_at')
        return queryset

class SearchView(generics.ListAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomUserFilter


# Comment
# [POST]: create comment, [GET]: comments list for post_id
class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        profile = self.request.user.profile
        content = request.data.get('content')
        comment = Comment.objects.create(post_id=post_id, author=profile, content=content)
        return Response(self.serializer_class(comment).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset=Comment.objects.filter(post__id=post_id)
        return queryset

# single comment [GET ,PUT, PATCH, DELETE]
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Reply
# [POST]: create reply, [GET]: replies list for comment_id
class ReplyView(generics.ListCreateAPIView):
    queryset=Reply.objects.all()
    serializer_class=ReplySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        comment_id = self.kwargs['comment_id']
        profile = self.request.user.profile
        content = request.data.get('content')
        if not content:
            return Response('content field required', status=status.HTTP_400_BAD_REQUEST)
        
        reply = Reply.objects.create(comment_id=comment_id, author=profile, content=content)
        return Response(self.serializer_class(reply).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        comment_id=self.kwargs['comment_id']
        queryset=Reply.objects.filter(comment__id=comment_id)
        return queryset

# single replies [GET ,PUT, PATCH, DELETE]
class ReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Reply.objects.all()
    serializer_class=ReplySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]


# Like 
# [POST, GET]
class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        profile = self.request.user.profile
        like = Like.objects.create(post_id=post_id, profile=profile)
        return Response(self.serializer_class(like).data, status=status.HTTP_201_CREATED)

# delete Likes
class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Saved Post
#[GET] list saved posts for auth user
class SavedPostView(generics.ListAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = SavedPost.objects.filter(profile=profile)
        return queryset
        
#[POST] save a post
class SavedPostCreateView(generics.CreateAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        profile = self.request.user.profile
        try:
            saved = SavedPost.objects.create(post_id=post_id, profile=profile)
            serializer = SavedPostSerializer(instance=saved, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "This post is already saved by the user."}, status=status.HTTP_400_BAD_REQUEST)

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


class HistoryView(generics.ListAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        queryset = SearchHistory.objects.filter(user=user)
        return queryset


class HistoryCreateView(generics.CreateAPIView):
    queryset=SearchHistory.objects.all()
    serializer_class=SearchHistorySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        print('first in def create')
        searched_username = request.data.get('searched_username')
        print(searched_username)
        if searched_username:
            searched_user=CustomUser.objects.get(username=searched_username)
            SearchHistory.objects.get_or_create(user=request.user, searched_user=searched_user)
            return self.get_response()
        
        return self.get_error_response()
    
    def get_response(self):
        return Response({"message": "Search history entry added successfully."}, status=status.HTTP_201_CREATED)

    def get_error_response(self):
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
class HistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=SearchHistory.objects.all()
    serializer_class=SearchHistorySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
