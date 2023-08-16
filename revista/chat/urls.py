from django.urls import path

from . import views

# 'chat/'
urlpatterns = [
    path('user/<int:profile_id>/', views.NewChat.as_view()),
    path('contact/', views.ChatContact.as_view()),
    path('all/', views.ChatView.as_view()),
    path('delete/<int:pk>/', views.ChatDeleteView.as_view()),
    path('messages/<int:chat_id>/', views.MessagesView.as_view()),
    path('forward/', views.ForwardMessage.as_view()),
    path('share-post/', views.SharePost.as_view()),
]