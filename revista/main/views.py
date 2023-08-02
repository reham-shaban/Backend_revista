from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from knox.auth import TokenAuthentication

from .models import Profile, Topic, TopicFollow, Follow
from .serializers import ProfileSerializer, VistorProfileSerializer, TopicSerializer, TopicFollowSerializer, FollowSerializer, FollowingListSerializer, FollowersListSerializer

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
        queryset = queryset.filter(follower=self.request.user.profile)
        return queryset 
              
# List my followers [GET]
class FollowersListView(generics.ListAPIView):
    serializer_class = FollowersListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Follow.objects.all()
        queryset = queryset.filter(followed=self.request.user.profile)
        return queryset