from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from users.managers import CustomeUserManager

class CustomeUser(AbstractUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('jobseeker', 'Jobseeker'),
        ('recruiter', 'Recruiter'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False)
    
    # Additional fields for job portal
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='jobseeker')
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomeUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
