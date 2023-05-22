from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    # path('social-django/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
]
