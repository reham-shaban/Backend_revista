import json
from django.views import generic, View
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Report, Warn
from posts.models import Post
from chat.models import Message
from .forms import ReportUpdateForm, WarnForm

# moderator screen (filter status, type from url)
class ReportList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Report
    template_name = 'report/report_list.html'
    context_object_name = 'reports'
    permission_required = 'report.view_report'
    
    def get_queryset(self):
        user_role = self.request.user.role
        # set status based on role
        if user_role == 'moderator':
            status = 'pending'
        elif user_role == 'admin':
            status = self.request.GET.get('status')
            if not status:
                status = 'redirected'
        else:
            return redirect(reverse('/'))
        
        # get queryset and filter status & type
        queryset = super().get_queryset()
        type = self.request.GET.get('type')
        
        if status:
            queryset = queryset.filter(status=status)
        if type:
            queryset = queryset.filter(type=type)
                     
        return queryset
    

class ReportDetail(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Report
    template_name = 'report/detail_base.html'
    permission_required = 'report.view_report'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = context['object']
        context['report_form'] = ReportUpdateForm(instance=context['object'])
        context['warn_form'] = WarnForm()
        
        # post object
        if report.reported_post:
            context['post'] = report.reported_post
        
        # messages
        if report.reported_chat:
            chat = report.reported_chat
            messages = Message.objects.filter(chat=chat)[:10]
            context['chat'] = chat
            context['messages'] = messages
            
        # Count the number of reports for the reported_user
        reported_user = context['object'].reported_user        
        report_count = Report.objects.filter(reported_user=reported_user).count()
        
        context['report_count'] = report_count
        return context
    
# delete post
class PostDeleteView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('report:reports')  # Redirect to report list page

# warn user
class WarnView(View):
    def post(self, request, pk): # report pk
        report = get_object_or_404(Report, pk=pk)
        warned_user = report.reported_user
        comment = request.POST.get('comment')
        print(comment)
        warn = Warn.objects.create(report=report, warned_user=warned_user, comment=comment)
        print(warn)
        return redirect('report:reports')
    