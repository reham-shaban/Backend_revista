from django.urls import path
from knox import views as knox_views

from . import views

# '/'
urlpatterns = [
    path('topics/', views.TopicView.as_view()),
    path('topics-follow/', views.TopicFollowView.as_view()),

]