from django.contrib import admin

from .models import Profile, UserStatus, Topic, TopicFollow, Follow, Block

# Register your models here.

admin.site.register(Profile)
admin.site.register(UserStatus)
admin.site.register(Topic)
admin.site.register(TopicFollow)
admin.site.register(Follow)
admin.site.register(Block)
