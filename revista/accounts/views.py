from django.contrib.auth import login, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.forms import ValidationError
import random, requests

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from knox.auth import TokenAuthentication

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from .models import CustomUser, PasswordResetCode
from .serializers import UserSerializer, RegisterSerializer, GoogleSignInSerializer

# # Login with google
# class GoogleSignInView(APIView):
#     def post(self, request):
#         serializer = GoogleSignInSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Verify the authenticityof the tokens
#         # access_token = serializer.validated_data['access_token']
#         id_token = serializer.validated_data['id_token']

#         # Verify the id_token with Google API
#         response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
#         if response.status_code != 200:
#             return Response({'error': 'Invalid id_token.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Extract the user information from the Google API response
#         user_data = response.json()
#         email = user_data.get('email')
#         google_id = user_data.get('sub')

#         # Authenticate the user
#         user = authenticate(request, email=email, google_id=google_id)
#         if user is None:
#             # Create a new user if the user does not exist
#             user = CustomUser.objects.create_user(email=email, google_id=google_id)

#         # Log the user in
#         login(request, user)

#         # Generate an auth token for the user
#         token, created = Token.objects.get_or_create(user=user)

#         # Return the response with the user ID and auth token
#         return Response({'user_id': user.id, 'auth_token': token.key})
     
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
        
# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    
# Reset password views
# 1.take the username and send an email
class ForgetPasswordView(APIView):
    def post(self, request):
        username = request.data.get('username')
        
        if not username:
            return Response({"error": "username required"}, status=status.HTTP_400_BAD_REQUEST)
       
        try:  
            user = CustomUser.objects.get(username=username)            
            id = user.id
            email = user.email
        except user.DoesNotExist:
            return Response({"error": "user with that username doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
          
        # Delete all old password reset codes for the user
        PasswordResetCode.objects.filter(user=user).delete()
             
        # create a new code   
        def generate_random_code():
            code = ""
            for i in range(6):
                code += str(random.randint(0, 9))
            return code
            
        code = generate_random_code()
        reset_code = PasswordResetCode.objects.create(user=user, code=code)
        
        # send an email
        subject = 'Verify Code'
        message = f'This is your verification code for revista: {code}\nif you haven\'t request for it, ignore it'
        from_email = 'settings.EMAIL_HOST_USER'
        recipient_list = [email]
           
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return Response({'id': id, 'email': email}, status=status.HTTP_200_OK)
  
# 2.check if the code is correct      
class CheckCodeView(APIView):
    def post(self, request):
        sent_code = request.data.get('code')
        if not sent_code:
            return Response({"error": "code required"}, status=status.HTTP_400_BAD_REQUEST)
         
        try:
            code = PasswordResetCode.objects.get(code=sent_code)
        except PasswordResetCode.DoesNotExist:
            return Response({"error": "wronge code"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message" : "successful"}, status=status.HTTP_200_OK)
        
# 3.reset the password in the database
class ResetPasswordView(APIView):
    def post(self, request):
        id = request.data.get('id')
        new_password = request.data.get('password')
        
        # checking for the input
        if not id:
            return Response({"error": "id required"}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({"error": "password required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.get(id=id)
        if user is None:
            return Response({"error": "No user exist with that id"}, status=status.HTTP_400_BAD_REQUEST)
        
        # password validation
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)
        
        # reset password
        user.set_password(new_password)
        user.save()
        
        return Response({"message" : "successful"}, status=status.HTTP_200_OK)

# List all users
class UserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


# Update User info
class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
