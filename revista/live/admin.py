from django.contrib import admin

from .models import Live, LiveComment

# Register your models here.
admin.site.register(Live)
admin.site.register(LiveComment)