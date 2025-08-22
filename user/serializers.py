# user\serializers.py

from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from cloudinary.utils import cloudinary_url

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'country_of_residence',
            'whatsapp_number',
            'email',
            'password',
            'confirm_password',
            'preferred_name',
            'certificate_name',
            'aice_id',
            'linkedin',
            'github',
            'profile_picture',
            'created_at',
            'updated_at',
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "password": "Your password and confirmation don’t match."
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            first_name=validated_data.get('first_name'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('last_name'),
            country_of_residence=validated_data.get('country_of_residence'),
            whatsapp_number=validated_data.get('whatsapp_number'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            preferred_name=validated_data.get('preferred_name'),
            certificate_name=validated_data.get('certificate_name'),
            aice_id=validated_data.get('aice_id'),
            linkedin=validated_data.get('linkedin'),
            github=validated_data.get('github'),
            profile_picture=validated_data.get('profile_picture'),
            created_at=validated_data.get('created_at'),
            updated_at=validated_data.get('updated_at'),
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'country_of_residence',
            'whatsapp_number',
            'created_at',
            'updated_at',
            'preferred_name',
            'certificate_name',
            'aice_id',
            'linkedin',
            'github',
            'profile_picture',
            'profile_picture_url',
        ]
    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            url, _=cloudinary_url(str(obj.profile_picture), secure=True)
            return url
        return None
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['name'] = user.first_name

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = UserSerializer(self.user).data

        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "password": "New password and confirm password don't match"
            })
        return attrs