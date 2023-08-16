from django.urls import path

from . import views

# 'live/'
urlpatterns = [
   path('', views.CreateLive.as_view()),
]