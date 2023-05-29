from django.urls import path
from knox import views as knox_views

from . import views

# 'auth/'
urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('forget-password/', views.ForgetPasswordView.as_view()),
    path('check-code/', views.CheckCodeView.as_view()),
    path('reset-password/', views.ResetPasswordView.as_view()),
   # path('google-login/', views.GoogleSignInView.as_view()),
   
   path('user-list/', views.UserView.as_view()),
   path('user-edit/', views.UserUpdateView.as_view()),
]