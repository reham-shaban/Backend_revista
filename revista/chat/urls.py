from django.urls import path

from . import views

'chat/'
urlpatterns = [
    path('user/<int:profile_id>/', views.NewChat.as_view()),
]