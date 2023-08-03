from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Report


# moderator screen (filter status, type from url)
class ReportList(LoginRequiredMixin, generic.ListView):
    model = Report
    context_object_name = 'reports'
    
    def get_queryset(self):
        user_role = self.request.user.role
        print(user_role)
        
        if user_role == 'moderator':
            status = 'pending'
        elif user_role == 'admin':
            status = self.request.GET.get('status')
        else:
            # Redirect to home page for other user roles
            return redirect(reverse('home'))
        
        queryset = super().get_queryset()
        type = self.request.GET.get('type')
        
        if status:
            queryset = queryset.filter(status=status)
        if type:
            queryset = queryset.filter(type=type)
                     
        return queryset
    
class ReportDetail(LoginRequiredMixin, generic.DetailView):
    model = Report