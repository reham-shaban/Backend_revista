from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .models import Live
from .serializers import LiveSerializer

# create Live
class LiveCreateView(generics.ListCreateAPIView):
    queryset = Live.objects.all()
    serializer_class = LiveSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
# delete Live
class LiveDeleteView(generics.DestroyAPIView):
    queryset = Live.objects.all()
    serializer_class = LiveSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
