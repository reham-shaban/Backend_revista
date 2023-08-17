from django.shortcuts import get_object_or_404
from django.db.models import Q, OuterRef, Subquery
from django.urls import reverse
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from knox.auth import TokenAuthentication

from accounts.models import CustomUser
from main.models import Profile, Block
from posts.models import Post
from .models import Chat, Message
from .serializers import ChatContactSerializer, ChatSerializer, MessageSerializer

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
    serializer_class = ChatContactSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Subquery to get the latest message creation time for each chat
        latest_message_subquery = Message.objects.filter(chat=OuterRef('pk')).order_by('-created_at')
        latest_message_time = Subquery(latest_message_subquery.values('created_at')[:1])
        
        queryset = Chat.objects.annotate(latest_message_time=latest_message_time)
        user = self.request.user
        profile = user.profile
        blocked_users = Block.objects.filter(blocker=profile).values_list('blocked', flat=True)
        blocked_by = Block.objects.filter(blocked=profile).values_list('blocker',flat=True)
        queryset = queryset.exclude(
        (Q(user1__profile=profile) & Q(user2__profile__in=blocked_users)) | 
        (Q(user1__profile=profile) & Q(user2__profile__in=blocked_by)) |
        (Q(user2__profile=profile) & Q(user1__profile__in=blocked_users)) | 
        (Q(user2__profile=profile) & Q(user1__profile__in=blocked_by)) |
        (Q(user1__is_active=False))|
        (Q(user2__is_active=False))
        )
        
        queryset = queryset.filter(Q(user1=user) | Q(user2=user))
        
        queryset = queryset.order_by('-latest_message_time')
        return queryset

# list all chats admin
class ChatView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
# delete chat
class ChatDeleteView(generics.DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
# get all messages from chat
class MessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        queryset = Message.objects.all()
        queryset = queryset.filter(chat_id=chat_id)
        return queryset
    
# forward message
class ForwardMessage(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = self.request.user
        message_id = request.POST.get('message_id')
        new_chat_id = request.POST.get('new_chat_id')
        
        if not message_id:
            return Response({'error': 'Missing message_id field.'}, status=status.HTTP_400_BAD_REQUEST)
        if not new_chat_id:
            return Response({'error': 'Missing new_chat_id field.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Retrieve the original message
        original_message = get_object_or_404(Message, id=message_id)
        
        # Create the forwarded message by copying the information from the original message
        forwarded_message = Message.objects.create(
            chat_id=new_chat_id,
            author=user,
            type=original_message.type,
            text=original_message.text,
            image=original_message.image,
            voice_record=original_message.voice_record,
            reaction=original_message.reaction,
            reply=original_message.reply,
        )
        return Response({'message': 'Message forwarded successfully.'}, status=status.HTTP_201_CREATED)

# share post to chat
class SharePost(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = self.request.user
        chat_id = request.POST.get('chat_id')
        post_id = request.POST.get('post_id')
        post_url = request.POST.get('post_url')
        
        if not chat_id:
            return Response({'error': 'Missing chat_id field.'}, status=status.HTTP_400_BAD_REQUEST)
        if not post_id:
            return Response({'error': 'Missing post_id field.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve chat and post
        chat = get_object_or_404(Chat, id=chat_id)
        post = get_object_or_404(Post, id=post_id)

        # Create the message
        message = Message.objects.create(
            chat_id=chat_id,
            author=user,
            type='text',
            text=post_url,
        )
        
        return Response({'message': 'Post shared successfully.'}, status=status.HTTP_201_CREATED)

        