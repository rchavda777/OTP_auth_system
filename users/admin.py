from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomeUser

class CustomUserAdmin(UserAdmin):
    model = CustomeUser
    list_display = ['email', 'full_name', 'phone_number','role', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', ]
    ordering = ['email']
    search_fields = ['email', 'full_name', 'phone_number']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': (
                'full_name',
                'phone_number',
                'bio',
                'gender',
                'date_of_birth',
                'address',
                'role',
            )
        }),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'full_name', 'phone_number', 'bio', 'gender',
                'date_of_birth', 'address', 'role',
                'is_staff', 'is_active'
            )
        }),
    )

admin.site.register(CustomeUser, CustomUserAdmin)
