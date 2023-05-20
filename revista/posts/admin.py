from django.contrib import admin

from .models import Post, Point, Like, Comment, Reply, SavedPost

# Register your models here.

admin.site.register(Post)
admin.site.register(Point)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(SavedPost)