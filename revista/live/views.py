from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Live

# views
class CreateLive(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        streamer = self.request.user
        live = Live.objects.create(streamer=streamer)
        
        return Response({"live_id": live.id}, status=status.HTTP_201_CREATED)
    