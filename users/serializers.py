from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'full_name', 'phone_number']

    def validate_email(self, value):
        """
        Validate that the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def validate_phone_number(self, value):
        """
        Validate that the phone number is unique.
        """
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phonr number already exists.")
        return value

    def validate(self, data):
        """
        Validate the password and confirm_password fields.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password and Confirm Password do not match.")
        return data

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']