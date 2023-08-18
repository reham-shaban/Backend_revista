from django.db import models
from django.core.validators import FileExtensionValidator

from accounts.models import CustomUser
from django.utils import timezone


REACTIONS = (
    (1, 'like'),
    (2, 'love'),
    (3, 'haha'),
    (4, 'wow'),
    (5, 'sad'),
    (6, 'angry')
)

TYPE = (
    ('text', 'Text'), ('image', 'Image'), ('voice_record', 'Voice Record')
)
    
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



class Call(models.Model):
    CALL_TYPE_CHOICES = (
        ('voice', 'Voice'),
        ('video', 'Video'),
    )
    
    call_type = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    caller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='outgoing_calls')
    callee = models.ForeignKey(CustomUser,null=False, on_delete=models.CASCADE, related_name='incoming_calls')
    on_call = models.BooleanField(default=False)

    def accept_call(self):
        self.on_call = True
        self.save()

    def end_call(self):
        self.on_call = False
        self.ended_at = timezone.now()
        self.save()
    
    def __str__(self):
        return f'{self.caller} {self.call_type} called {self.callee}'