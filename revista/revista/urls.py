from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2CallbackView,
    OAuth2LoginView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # allauth library
    # path('accounts/google/login/', OAuth2LoginView.as_view()),
    # path('accounts/google/callback/', OAuth2CallbackView.as_view(adapter=GoogleOAuth2Adapter)),
    
    # local
    path('auth/', include('accounts.urls')),
    path('', include('main.urls')),
    path('posts/', include('posts.urls')),
    # path('social-django/', include('social_django.urls', namespace='social')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

