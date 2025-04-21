from django.contrib.auth.base_user import BaseUserManager

class CustomeUserManager(BaseUserManager):
    """
    Custome user manager for creating users and superusers.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and retuen a user with an email and password.
        """
        
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The password field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and retuen a superuser with an email amnd password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
