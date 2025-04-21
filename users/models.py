from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from users.managers import CustomeUserManager
#from .managers import CustomUserManager

class CustomeUser(AbstractUser):
    """
    Custom user model that extends the default Django user models.
    """
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email' # The field to use as the unique identifier for authentication
    REQUIRED_FIELDS = []
    
    objects = CustomeUserManager() # Use the custom user manager for creating users and superusers

    def __str__(self):
        return self.email