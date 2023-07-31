from django.urls import path
from . import views

urlpatterns = [
    # post
    path('', views.HomePostView.as_view(),name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view()),
    path('all/', views.PostView.as_view()),
    path('timeline/',views.MyTimeLineView.as_view()),
    path('timeline/<int:profile_id>',views.TimeLineView.as_view()),
    
    # discover page
    path('discover/<int:topic_id>/',views.DiscoverView.as_view(),name='discover-topic'),
    path('general/',views.GeneralView.as_view(),name='general-posts'),
    path('search/',views.SearchView.as_view(),name='search-users'),
    
    # comment
    path('comments/<int:post_id>/',views.CommentView.as_view(),name='add-comment'),
    path('comment/<int:pk>/', views.CommentDetailView.as_view()),
    
    # reply
    path('replies/<int:comment_id>/',views.ReplyView.as_view(),name='replies'),
    path('reply/<int:pk>/',views.ReplyDetailView.as_view(),),
    
    # like
    path('like/<int:post_id>/',views.LikeView.as_view()),
    path('unlike/<int:pk>/',views.LikeDeleteView.as_view()),
    
    # saved posts
    path('saved-posts/',views.SavedPostView.as_view(),name='savedposts'),
    path('save-post/<int:post_id>/',views.SavedPostCreateView.as_view(),name='save'),
    path('saved-post/<int:saved_post_id>/', views.SavedPostDetailView.as_view(), name='savedpost-detail'),
     
]


