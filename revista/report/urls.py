from django.urls import path
from . import views

app_name = 'report'

'report/'
urlpatterns = [
   path('', views.ReportList.as_view(), name='reports'), # '/report/?status=pending&type=user'
   path('<int:pk>', views.ReportDetail.as_view(), name='report-detail'),
   path('mod-comment/<int:report_id>', views.mod_comment, name='mod-commnet'),
   path('ban', views.ban_page, name='ban-page'),
   
   # actions
   path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
   path('warn/<int:pk>/', views.WarnView.as_view(), name='warn-user'),
   path('decline/<int:pk>/', views.DeclineView.as_view(), name='decline'),
   path('redirect/<int:pk>/', views.RedirectView.as_view(), name='redirect'),
   path('ban/<int:pk>/', views.BanUserView.as_view(), name='ban'),

]
