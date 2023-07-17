from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

# urls
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('main.urls')),
    path('auth/', include('accounts.api.urls')),
    path('accounts/', include('accounts.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include("chat.urls")),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Customize admin site
admin.site.site_header  =  "Revista"  
admin.site.site_title  =  "revista site"
admin.site.index_title  =  "revista admin site"