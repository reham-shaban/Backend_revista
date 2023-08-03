from django.urls import path
from . import views

app_name = 'report'

'report/'
urlpatterns = [
   path('', views.ReportList.as_view(), name='reports'), # '/report/?status=pending&type=user'
   path('<int:pk>', views.ReportDetail.as_view(), name='report-detail'),
]
