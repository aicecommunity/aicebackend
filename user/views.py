# user\views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView

import cloudinary

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
    