from django.urls import path

from . import views

# 'live/'
urlpatterns = [
   path('', views.LiveCreateView.as_view()),
   path('close/<int:pk>', views.LiveDeleteView.as_view()),
]