from django.urls import path
from . import views

urlpatterns = [
    #posts [POST, GET]get a list of posts
    path('list-posts/', views.PostListCreateView.as_view(),name='home'),
    #[GET ,PUT, PATCH, DELETE]
    path('read-post/<int:pk>/', views.PostDetailView.as_view()),
    
    #comments
        #both create and get a list of comments
    path('create-comments/<int:post>/',views.CommentCreateView.as_view(),name='add-comment'),
        #[GET ,PUT, PATCH, DELETE]
    path('read-comment/<int:pk>/', views.CommentDetailView.as_view()),
    
    #Like
    path('like-post/',views.LikeCreateView.as_view()),
    path('<int:pk>/unlike-post/',views.LikeDeleteView.as_view()),
    
    #saved posts
    #[POST, GET] get list of posts
    path('list-savedposts/',views.SavedPostListCreateView.as_view(),name='savedposts'),
    #[GET, DELETE] get a single saved post
    path('savedpost/<int:profile_id>/<int:post_id>/', views.SavedPostDetailView.as_view(), name='savedpost-detail'),
    
    
]


