from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
