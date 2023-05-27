from django.urls import path
from knox import views as knox_views

from . import views

# '/'
urlpatterns = [
    path('topics/', views.TopicListView.as_view()),
    path('topics-follow/', views.TopicFollowView.as_view()),
    path('profile-list/', views.ProfileView.as_view()),
    path('profile-edit/<int:pk>', views.ProfileUpdateView.as_view()),
]