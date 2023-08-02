from django.urls import path

from . import views

# 'report-app/'
urlpatterns = [
   path('', views.ReportView.as_view()),
]