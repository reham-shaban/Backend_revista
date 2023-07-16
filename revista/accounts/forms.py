from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'username', 'email', 'first_name', 'last_name', 'birth_date', 'phone_number', 'gender']