from django.db import models

from accounts.models import CustomUser
from posts.models import Post

TYPE = {
    ('user', 'User'), ('post', 'Post'), ('chat', 'Chat')
}

CATEGORY = {
    ('harassment', 'Harassment'), ('spam', 'Spam'), ('inappropriate-content', 'Inappropriate content')
}

STATUS = {
    ('pending', 'Pending'), ('resolved', 'Resolved'), ('redirected', 'Redirected')
}

# Create your models here.
class Report(models.Model):
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reporter')
    type = models.CharField(max_length=25, choices=TYPE)
    category = models.CharField(max_length=25, choices=CATEGORY)
    reported_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reported_user')
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS, default='pending')
    reported_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reported_post', null=True, blank=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='moderator', null=True, blank=True)
    moderator_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.type} : {self.description}'

class Warn(models.Model):
    warned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='warned_user')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)