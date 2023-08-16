import random, requests, io
from django.forms import ValidationError
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.files.storage import FileSystemStorage
from django.core.validators import EmailValidator

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from ..models import CustomUser, PasswordResetCode, EmailChangeCode
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer

# Google
def download_image(profile_url, username):
    response = requests.get(profile_url) 
    response.raise_for_status()
    file_content = io.BytesIO(response.content)
    fs = FileSystemStorage()
    profile_image = fs.save(f'{username}_profile_image.jpg', file_content)
    return profile_image

class GoogleView(APIView):
    def post(self, request):
        info = request.data.get('info')
        email = info['email']
        
        # Check if account already exist
        user = CustomUser.objects.filter(email=email).first()
        
        if user is None:
            # Create new account               
            username = CustomUser.generate_username(email)
            password = CustomUser.objects.make_random_password()            
            profile_url = info['photoUrl']
            profile_image = download_image(profile_url, username)            
            name = info['displayName']
            first_name = name.split(' ')[0]
            last_name = name.split(' ')[1]
                    
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=password, 
                profile_image=profile_image,
                first_name=first_name,
                last_name=last_name,
                )
            user.save()
            login(request, user)
            message = 'User created and logged in successfully'
        else:    
            login(request, user)
            message = 'User logged in successfully'
            
        # Create token
        token = AuthToken.objects.create(user)[1]
        id = user.id
        
        return Response({
            'message': message,
            'token': token,
            'id': id
        })       

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
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            try:
                userObj = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return Response('username does not exist', status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user not active
            if not userObj.is_active:
                print("not active")
                userObj.is_active = True
                userObj.save()               

            # login
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            token = AuthToken.objects.create(user)
            return Response(
                {
                    'token': token[1],
                    'id': user.id,
                    'profile_id': user.profile.id,
                },
                status=status.HTTP_200_OK
            )
        else:       
            return Response('Invalid request, enter username and password!', status=status.HTTP_400_BAD_REQUEST)


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

# Update last online
class UpdateLastOnline(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = self.request.user
        print(user)
        user.last_online = timezone.now()
        user.save()
        return Response({'message': 'Online status updated.'}, status=status.HTTP_200_OK)

# Deactivate account
class DeactivateAccountView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer  

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'message': 'Account deactivated successfully'})

# Change Email views
class ChangeEmailView(APIView):
    def post(self,request):
        username=request.data.get('username')
        new_email=request.data.get('email')
        if not username:
            return Response({"error": "username required"}, status=status.HTTP_400_BAD_REQUEST)
        try:  
            user = CustomUser.objects.get(username=username)            
            id = user.id
        except user.DoesNotExist:
            return Response({"error": "user with that username doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        EmailChangeCode.objects.filter(user=user).delete()
        def generate_random_code():
                    code = ""
                    for i in range(6):
                        code += str(random.randint(0, 9))
                    return code

        code = generate_random_code()
        reset_code = EmailChangeCode.objects.create(user=user, code=code)


        subject = 'Verify Code For Email Change'
        message = f'This is your verification code for revista: {code}\nif you haven\'t request for it, ignore it'
        from_email = 'settings.EMAIL_HOST_USER'
        recipient_list = [new_email]
           
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return Response({'id': id, 'email': new_email}, status=status.HTTP_200_OK)

class CheckEmailCodeView(APIView):
    def post(self, request):
        sent_code = request.data.get('code')
        if not sent_code:
            return Response({"error": "code required"}, status=status.HTTP_400_BAD_REQUEST)
         
        try:
            code = EmailChangeCode.objects.get(code=sent_code)
        except EmailChangeCode.DoesNotExist:
            return Response({"error": "wronge code"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message" : "successful"}, status=status.HTTP_200_OK)
        
class ResetEmailView(APIView):
    def post(self, request):
        id= request.data.get('id')
        new_email=request.data.get('email')
        
        if not id:
            return Response({"error": "id required"}, status=status.HTTP_400_BAD_REQUEST)
        if not new_email:
            return Response({"error": "password required"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=id)
        if user is None:
            return Response({"error": "No user exist with that id"}, status=status.HTTP_400_BAD_REQUEST)
        
        email_validator = EmailValidator(message="Enter a valid email address.")
        
        try:
            email_validator(new_email)
        except ValidationError as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        user.email = new_email
        user.save()
        
        return Response({"message": "Email changed successfully"}, status=status.HTTP_200_OK)
     