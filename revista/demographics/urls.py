from django.urls import path
from . import views

#'demographics'
urlpatterns = [
path('age-stats/',views.AgeView.as_view(),name='Age'),
    path('gender-stats/',views.GenderView.as_view(),name='Gender'),
    path('trending-topics-stats/', views.TrendingTopicsView.as_view(),name='Trending topics'),
    path('topics_activitiy_stats/',views.TopicsActivityView.as_view(),name='Topics activity'),
    path('topics-followings-stats/',views.TopicsFollowingsStatsView.as_view(),name='Topics followings'),
]