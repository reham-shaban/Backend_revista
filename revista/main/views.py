from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .models import Topic, TopicFollow
from .serializers import TopicSerializer, TopicFollowSerializer

# List Topics
class TopicView(generics.ListAPIView):
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

