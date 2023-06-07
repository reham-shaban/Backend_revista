from django.db import models
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    cover_image = models.ImageField(default='cover_images/default.jpg', upload_to='cover_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
              
    def __str__(self):
      return f'{self.user.username} profile'

class UserStatus(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='status')
    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.profile.user.username} ({self.profile.id})'

    class Meta:
        verbose_name_plural = "User statuses"

class Topic(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='topics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def delete(self, *args, **kwargs):
        # Remove the image file if it exists
        if self.image:
            storage, path = self.image.storage, self.image.path
            storage.delete(path)

        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name

class TopicFollow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
      
    class Meta:
        verbose_name_plural = "Topics Follow"
        constraints = [
            models.UniqueConstraint(fields=['profile', 'topic'], name='unique_profile_topic')
        ]
        
    def __str__(self):
        return f'{self.profile.user.username} {self.topic}'

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followerd')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follower_followed')
        ]
        
    def __str__(self):
        return f'{self.follower} is following {self.followed}'
        

class Block(models.Model):
    blocker = models.ForeignKey(Profile, related_name='blocker', on_delete=models.CASCADE)
    blocked = models.ForeignKey(Profile, related_name='blocked', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
