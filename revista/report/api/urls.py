from django.urls import path

from . import views

# 'report-app/'
urlpatterns = [
   path('', views.ReportView.as_view()),
   path('warn-detail/<int:pk>/', views.WarnDetailView.as_view()),
]