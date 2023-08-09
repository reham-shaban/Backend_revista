# forms.py
from django import forms
from .models import Report, Warn

class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['moderator_comment']

class WarnForm(forms.ModelForm):
    class Meta:
        model = Warn
        fields = ['comment']