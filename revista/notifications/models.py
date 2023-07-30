from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='notifications/', blank=True, null=True)
    type = models.CharField(max_length=25) # (Follow, Post, Reply, Chat)
    detail = models.TextField()
    forward_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.type} notification for {self.user}'
