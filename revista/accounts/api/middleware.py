from django.http import Response
from django.contrib.auth import logout

class AccountDeactivationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if user is authenticated and deactivated
        if request.user.is_authenticated and not request.user.is_active:
            # Clear user-related data from the response
            logout(request)
            return Response({"message": "Account deactivated successfully!"}, status=200)
        return response