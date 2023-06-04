from django.urls import path

from . import views

# 'notifications/'
urlpatterns = [
    path('list/', views.NotificationListView.as_view()),
]