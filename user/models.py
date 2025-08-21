# user\models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime
from cloudinary.models import CloudinaryField

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    country_of_residence = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    preferred_name = models.CharField(max_length=100, blank=True, null=True)
    certificate_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    aice_id = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    github = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = CloudinaryField('image', blank=True, null=True)
     

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.preferred_name:
            self.preferred_name = self.first_name

        if not self.certificate_name:
            full_middle = f" {self.middle_name}" if self.middle_name else ""
            self.certificate_name = f"{self.first_name}{full_middle} {self.last_name}".strip()
        
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.aice_id:
            self.aice_id = f"AiCE/{datetime.date.today().year}/{self.id}"
            super().save(update_fields=['aice_id'])
        

    def __str__(self):
        return self.email