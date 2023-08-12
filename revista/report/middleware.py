from django.http import JsonResponse
from django.contrib.auth import logout
from django.urls import reverse

class BanCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user is banned
        if request.user.is_authenticated and request.user.is_banned:
            # Logout the banned user
            logout(request)
            
            # Return a JSON response indicating the user is banned
            return JsonResponse({"message": "You are banned."}, status=403)
        
        return response
