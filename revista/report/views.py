from django.views import generic
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Report
from posts.models import Post
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
    permission_required = 'report.view_report'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = context['object']
        context['report_form'] = ReportUpdateForm(instance=context['object'])
        context['warn_form'] = WarnForm()
        
        if report.reported_post:
            context['post'] = report.reported_post
            
        # Count the number of reports for the reported_user
        reported_user = context['object'].reported_user        
        report_count = Report.objects.filter(reported_user=reported_user).count()
        
        context['report_count'] = report_count
        return context
 
    def post(self, request, *args, **kwargs):
        report = self.get_object()
        form_type = request.POST.get('form_type')
        
        if form_type == 'report':
            report_form = ReportUpdateForm(request.POST, instance=report)
            if report_form.is_valid():
                report_form.save()
                return redirect('report:report-detail', pk=report.pk)
            
        elif form_type == 'warn':
            warn_form = WarnForm(request.POST)
            if warn_form.is_valid():
                warn = warn_form.save(commit=False)
                warn.report = report
                warn.warned_user = report.reported_user
                warn.save()
                return redirect('report:report-detail', pk=report.pk)
            
        elif form_type == 'redirect':
            report.status = 'redirected'
            report.save()
            return redirect('report:report-detail', pk=report.pk)
        
        context = self.get_context_data(report_form=report_form, warn_form=warn_form)
        return self.render_to_response(context)

  
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Post
    permission_required = 'posts.delete_post'
    template_name = 'report/report_list.html'
    success_url = reverse_lazy('report:reports')  # Redirect to a list view after deletion
