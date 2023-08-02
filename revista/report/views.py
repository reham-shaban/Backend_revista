from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Report


# moderator screen (filter status, type from url)
class ReportList(LoginRequiredMixin, generic.ListView):
    model = Report
    context_object_name = 'reports'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        type = self.request.GET.get('type')
        
        if status:
            queryset = queryset.filter(status=status)
        if type:
            queryset = queryset.filter(type=type)
                     
        return queryset
    