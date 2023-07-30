from django.urls import path
from . import views

urlpatterns = [
    #posts [POST, GET]get a list of posts
    path('', views.HomePostView.as_view(),name='home'),
    #[GET ,PUT, PATCH, DELETE]
    path('post/<int:pk>/', views.PostDetailView.as_view()),
    path('all/', views.PostView.as_view()),
    
    #comments
        #both create and get a list of comments
    path('comments/<int:post_id>/',views.CommentView.as_view(),name='add-comment'),
        #[GET ,PUT, PATCH, DELETE]
    path('comment/<int:pk>/', views.CommentDetailView.as_view()),
    
    #replies
        #both create and get a list of replies
    path('replies/<int:comment_id>/',views.ReplyView.as_view(),name='replies'),
        #[GET ,PUT, PATCH, DELETE]
    path('reply/<int:pk>/',views.ReplyDetailView.as_view(),),
    
    #Like
    path('like/<int:post_id>/',views.LikeView.as_view()),
    path('unlike/<int:pk>/',views.LikeDeleteView.as_view()),
    
    #saved posts
    #[GET] get list of posts
    path('saved-posts/',views.SavedPostView.as_view(),name='savedposts'),
    #[POST]
    path('save-post/<int:post_id>/',views.SavedPostCreateView.as_view(),name='save'),
    #[GET, DELETE] get a single saved post
    path('saved-post/<int:saved_post_id>/', views.SavedPostDetailView.as_view(), name='savedpost-detail'),
]


