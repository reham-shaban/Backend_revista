from django.urls import path
from knox import views as knox_views

from . import views

# '/'
urlpatterns = [
    path('topics/', views.TopicListView.as_view()),
    path('topics-follow/', views.TopicFollowView.as_view()),
    path('topics-unfollow/<int:pk>', views.TopicUnFollowView.as_view()),
    
    path('profile-list/', views.ProfileView.as_view()),
    path('profile/<int:pk>', views.SingleProfileView.as_view()),
    path('my-profile/', views.ProfileUpdateView.as_view()),
    
    path('follow/', views.FollowView.as_view()),
    path('unfollow/<int:pk>', views.UnFollowView.as_view()),
    path('following-list/', views.FollowingListView.as_view()),
    path('followers-list/', views.FollowersListView.as_view()),
    
    path('block-list/',views.BlockedUsers.as_view()),
    path('block-user/',views.BlockUsers.as_view()),
    path('unblock-user/<int:pk>/',views.UnblockUsers.as_view()),
    

]