from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterForm
from .models import CustomUser

# Create your views here.
# Login
class LoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/report/'
    
# Logout
@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

    
# Register
class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        # authenticate user and log them in
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return redirect('/')