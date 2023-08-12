from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import random

# Create your models here.
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)
    
ROLE = (
    ('admin', 'Admin'), ('moderator', 'Moderator'), ('regular-user', 'Regular User')
)
    
class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    profile_image = models.ImageField(default='profile_images/default.png', upload_to='profile_images/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
    role = models.CharField(max_length=25, choices=ROLE, default='regular-user')
    is_online = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
        
    def __str__(self):
        return self.username
    
    @staticmethod
    def generate_username(email):
        username = email.split('@')[0]
        username = "".join([c for c in username if c.isalpha()])
       
        # Check if username exist
        while CustomUser.objects.filter(username=username).exists():
            username = "{0}{1}".format(username, random.randint(0, 9))
       
        return username
    
    
class PasswordResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:  # Only set expires_at when creating a new instance
            self.expires_at = timezone.now() + timezone.timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f'code: {self.code}'
  
       
class EmailChangeCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:  # Only set expires_at when creating a new instance
            self.expires_at = timezone.now() + timezone.timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f'code: {self.code}'
   