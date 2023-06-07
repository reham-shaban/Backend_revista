from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.
GENDER_CHOICES = {
    ('M', 'Male'),
    ('F', 'Female'),
}

class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    profile_image = models.ImageField(default='profile_images/default.png', upload_to='profile_images/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
        
    def __str__(self):
        return self.username
    
class PasswordResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=30))
         
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f'code: {self.code}'
   