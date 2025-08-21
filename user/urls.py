# user\urls.py

from django.urls import path
from .views import SignupAPIView
from user.views import CustomTokenObtainPairView, CustomLoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', CustomLoginAPIView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]