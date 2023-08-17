from django.db import models

from accounts.models import CustomUser

# Create your models here.
class Live(models.Model):
    streamer = models.ForeignKey(CustomUser, related_name='streamer', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.streamer}'s live"
    
    
# class LiveComment(models.Model):
#     live = models.ForeignKey(Live, on_delete=models.CASCADE)
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.author.user}: {self.content}"
    