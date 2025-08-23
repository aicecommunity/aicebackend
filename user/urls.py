# user\urls.py

from django.urls import path
from .views import SignupAPIView
from user.views import CustomTokenObtainPairView, CustomLoginAPIView, LogoutView, ProfileView, ChangePasswordView, request_verification_code, verify_code, request_free_email_code, verify_free_email_code, send_karibu_mail
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', CustomLoginAPIView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('request-code/', request_verification_code, name='request-code'),
    path('verify-code/', verify_code, name='verify-code'),
    path('request-free-code/', request_free_email_code, name='request-free-code'),
    path('verify-free-code/', verify_free_email_code, name='verify-free-code'),
    path('send-karibu-mail/', send_karibu_mail, name='send-karibu-mail'),
]