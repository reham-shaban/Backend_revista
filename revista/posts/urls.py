from django.urls import path
from . import views



urlpatterns = [
    #posts
    path('list-posts/', views.PostListView.as_view(),name='home'),
    path('read-posts/<int:pk>/', views.PostDetailView.as_view()),
    path('create-posts/', views.PostCreateView.as_view()),
    path('<int:pk>/delete-posts/', views.PostDeleteView.as_view()),
    path('<int:pk>/update-posts/',views.PostUpdateView.as_view()),
    #comments
    path('create-comments/<int:post>/',views.CommentCreateView.as_view(),name='add-comment'),
    path('list-comments/<int:post>/', views.CommentListView.as_view(),name='Comments'),
    path('read-comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('<int:pk>/delete-comments/', views.CommentDeleteView.as_view()),
    path('<int:pk>/update-comments/',views.CommentUpdateView.as_view()),
    #saved posts
    path('list-saved-posts/', views.SavedPostListView.as_view(),name='saved'),
    path('read-saved-posts/<int:pk>/', views.SavedPostDetailView.as_view()),
    path('save-posts/', views.SavedPostCreateView.as_view()),
    path('<int:pk>/unsave-posts/', views.SavedPostDeleteView.as_view()),
]


