from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knox.auth import TokenAuthentication

from ..models import Report, Warn
from .serializers import ReportSerializer, WarnSerializer

# Create your views here.
class ReportView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class WarnDetailView(generics.RetrieveAPIView):
    queryset = Warn.objects.all()
    serializer_class = WarnSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
