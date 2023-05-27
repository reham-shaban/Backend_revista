from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from knox.auth import TokenAuthentication

from .models import Profile, Topic, TopicFollow
from .serializers import ProfileSerializer, TopicSerializer, TopicFollowSerializer

# List all Profiles
class ProfileView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

# Update Profile
class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
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

