from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from knox.auth import TokenAuthentication
from django.db import IntegrityError
from .models import Profile, Topic, TopicFollow, Follow,Block
from .serializers import ProfileSerializer, VistorProfileSerializer, TopicSerializer, TopicFollowSerializer, FollowSerializer, FollowingListSerializer, FollowersListSerializer, BlockSerializer, BlockedListSerializer

# Profile
# List all Profiles
class ProfileView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

# Update My Profile [GET, PATCH]
class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile

# Retrieve single Profile with id
class SingleProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = VistorProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Topics
# List Topics
class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Follow Topics [GET, POST]
class TopicFollowView(generics.ListCreateAPIView):
    serializer_class = TopicFollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TopicFollow.objects.filter(profile__user=user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile
        serializer.save(profile=profile)

class TopicUnFollowView(generics.DestroyAPIView):
    queryset = TopicFollow.objects.all()
    serializer_class = TopicFollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Follow
# Follow someone [POST]
class FollowView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user.profile)

# UnFollow someone [DELETE]
class UnFollowView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

# List my following [GET]
class FollowingListView(generics.ListAPIView):
    serializer_class = FollowingListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Follow.objects.all()
        profile=self.request.user.profile
        queryset = queryset.filter(follower=profile)
        blocked = Block.objects.filter(blocker=profile).values_list('blocked', flat=True)
        blocked_by=Block.objects.filter(blocked=profile).values_list('blocker', flat=True)
        queryset = queryset.exclude(followed__id__in=blocked)
        queryset = queryset.exclude(followed__id__in=blocked_by)
        return queryset 
        
# List my followers [GET]
class FollowersListView(generics.ListAPIView):
    serializer_class = FollowersListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile=self.request.user.profile
        queryset = Follow.objects.all()
        queryset = queryset.filter(followed=self.request.user.profile)
        blocked = Block.objects.filter(blocker=profile).values_list('blocked', flat=True)
        blocked_by=Block.objects.filter(blocked=profile).values_list('blocker', flat=True)
        queryset = queryset.exclude(follower__id__in=blocked)
        queryset = queryset.exclude(follower__id__in=blocked_by)  
        return queryset
    
    
# List Blocked users
class BlockedUsers(generics.ListAPIView):
    serializer_class=BlockedListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=Block.objects.all()
        queryset=queryset.filter(blocker=self.request.user.profile)
        return queryset
    

class BlockUsers(generics.CreateAPIView):
    queryset = Block.objects.all()
    serializer_class=BlockSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)  # This will raise a validation error if needed
        try:
            serializer.save(blocker=self.request.user.profile)
        except IntegrityError:
            return Response({"error": "User already blocked."}, status=status.HTTP_400_BAD_REQUEST)
        

class UnblockUsers(generics.DestroyAPIView):
    queryset = Block.objects.all()
    serializer_class=BlockSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]