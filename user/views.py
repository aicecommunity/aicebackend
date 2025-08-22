# user\views.py

from rest_framework import generics, status, permissions, views
from .serializers import UserSignupSerializer, CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
import cloudinary
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import send_verification_code
from django.utils import timezone
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives



cloudinary.config(
    cloud_name='drw7rsyaa',
    api_key='376849678198392',
    api_secret='me-7bYJPpXJdPuJJlAJM6KcrqQo',
)

# Create your views here.
class SignupAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignupSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomLoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'detail': 'Successfully logged out'
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({
                "error": "Invalid Token or already blacklisted."
            }, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    # GET, PUT/PATCH, DELETE
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):

        serializer = UserSerializer(
            self.get_object(),
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(
            {"detail": "Your account has been deleted."},
            status=status.HTTP_204_NO_CONTENT
        )
    
class ChangePasswordView(generics.UpdateAPIView):
    # PUT
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set the new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, user)

        return Response(
            {"details": "Password updated successfully."},
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
def request_verification_code(request):
    email = request.data.get('email')
    try:
        user = CustomUser.objects.get(email=email)
        send_verification_code(user)
        return Response({
            "message": "Verification code sent to your email."
        })
    except CustomUser.DoesNotExist:
        return Response({
            "error": "User with this email does not exist."
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def verify_code(request):
    email = request.data.get('email')
    code = request.data.get('code')

    try:
        user = CustomUser.objects.get(email=email)

        if (user.verification_code == code and 
                user.code_expiry and
                user.code_expiry > timezone.now()
                ):
            user.verification_code = None
            user.code_expiry = None
            user.save()
            return Response({
                "message": "Verification successful."
            })
        else:
            return Response({
                "error": "Invalid or expired code."
            }, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({
            "error": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)

# FOR FREE VERIFICATION
@api_view(['post'])
def request_free_email_code(request):
    email = request.data.get('email')
    if not email:
        return Response({
            "error": "Email is required."
        }, status=status.HTTP_400_BAD_REQUEST)
    from .utils import generate_verification_code
    code = generate_verification_code()
    cache.set(f'verify_code_{email}', code, timeout=6000)

    subject = "AiCE Verification Code"
    from_email = "aicecommunity@gmail.com"
    to = [email]

    text_content = f"Your verification code is {code}. It will expire in 10 minutes."

    with open('email_code.html', 'r', encoding='utf-8') as my_file:
        html_content = my_file.read()
    
    html_content = html_content.format(first_name='', code=code)

    email_msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()

    return Response({"message": "Verification code sent to your email."})


@api_view(['POST'])
def verify_free_email_code(request):
    email = request.data.get('email')
    code = request.data.get('code')

    if not email or not code:
        return Response({"error": "Email and code are required."}, status=status.HTTP_400_BAD_REQUEST)

    stored_code = cache.get(f'verify_code_{email}')

    if stored_code and stored_code == code:
        # Clear code after successful verification
        cache.delete(f'verify_code_{email}')
        return Response({"message": "Verification successful."})

    return Response({"error": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)