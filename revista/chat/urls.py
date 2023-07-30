from django.urls import path

from . import views

'chat/'
urlpatterns = [
    path('user/<int:profile_id>/', views.NewChat.as_view()),
    path('contact/', views.ChatContact.as_view()),
    path('all/', views.ChatView.as_view()),
    path('delete/<int:pk>/', views.ChatDeleteView.as_view()),
]