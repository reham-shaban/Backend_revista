from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from accounts.models import CustomUser
from main.models import Profile
from .models import Chat
from .serializers import ChatSerializer

# APIs
# get or create chat throw profile id
class NewChat(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, profile_id):       
        # get authenticated user and user selected in url
        user1 = self.request.user
        profile = get_object_or_404(Profile, id=profile_id) # in url there is profile id
        user2 = get_object_or_404(CustomUser, id=profile.user.id)
            
        # get the chat between the two users or create one
        chat = Chat.objects.filter(user1=user1, user2=user2).first() \
           or Chat.objects.filter(user1=user2, user2=user1).first()

        if not chat:
            chat = Chat.objects.create(user1=user1, user2=user2)
            
        return Response({"chat_id": chat.id}, status=status.HTTP_201_CREATED)

# get contact screen
class ChatContact(generics.ListAPIView):
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Chat.objects.all()
        user = self.request.user
        queryset = queryset.filter(Q(user1=user) | Q(user2=user))
        return queryset
