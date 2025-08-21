# user\admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'first_name',
        'middle_name',
        'last_name',
        'country_of_residence',
        'whatsapp_number',
        'email',
        'profile_picture',
        'preferred_name',
        'certificate_name',
        'aice_id',
        'linkedin',
        'github',
        'created_at',
        'updated_at',
        'is_staff'
    )

    ordering = ('email',)

    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('middle_name', 'country_of_residence', 'whatsapp_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)