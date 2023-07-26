from django.db import models
from django.core.validators import FileExtensionValidator

from accounts.models import CustomUser

REACTIONS = {
    (1, 'like'),
    (2, 'love'),
    (3, 'haha'),
    (4, 'wow'),
    (5, 'sad'),
    (6, 'angry')
}

TYPE = {
    ('text', 'Text'), ('image', 'Image'), ('voice_record', 'Voice Record')
}

class Chat(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='user1', null=True, on_delete=models.SET_NULL)
    user2 = models.ForeignKey(CustomUser, related_name='user2', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user1} - {self.user2}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='author', null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=20, choices=TYPE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    voice_record = models.FileField(upload_to='voice_records/', blank=True, null=True, validators=[FileExtensionValidator(['wav', 'mp3'])])
    reaction = models.IntegerField(blank=True, null=True, choices=REACTIONS)
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author}: {self.type} "{self.text}"'
    