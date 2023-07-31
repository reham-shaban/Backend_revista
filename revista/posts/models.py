from django.db import models

from main.models import Profile, Topic

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    content = models.TextField()
    link = models.URLField(blank=True, null=True)
    topics = models.ManyToManyField(Topic)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.user}: {self.content}"


class Point(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pointed_post')
    value = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.value} : {self.post.author.user}: {self.post.content}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='liked_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('post', 'profile')
    
    def __str__(self):
        return f"{self.profile.user} liked {self.post.author.user}'s post"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commented_post')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_author')
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.author.user}: {self.content}"
    

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replied_comment')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reply_author')
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.author.user}: {self.content}"
    
    class Meta:
        verbose_name_plural = "Replies"


class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_saved')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('post', 'profile')
        
    def __str__(self):
        return f"{self.post.author.user}: {self.post.content}"
