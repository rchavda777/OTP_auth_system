import os, random
import requests
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny 
from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer, LoginSerializer
from .utils.generate_reset_token import generate_reset_token, decode_reset_token


load_dotenv()
User = get_user_model()
OTP_EXPIRY_SECONDS = 600 # 10 minutes
MAX_OTP_ATTEMPTS = 3

def validate_email_with_mailboxlayer(email):
    """
    validate email is abel to recieve email or not using mailboxlayer API
    """

    api_key = os.getenv('MAILBOXLAYER_API_KEY')
    if not api_key:
        raise ValueError("Mailbox Layer API keyv not found in environment variables, please set it up.")
    
    url = f"http://apilayer.net/api/check?access_key={api_key}&email={email}&smtp=1&format=1"
    try:
        response = requests.get(url).json()
        if response.get("smtp_check"):
            return True
        else:
            return False, "Invalid email address."
    except requests.ResponseError as e:
        return False, f"Email validation failed: {e}"
    
def generate_and_send_otp(email):
    otp = str(random.randint(100000, 999999))
    
    try:
        send_mail(
            subject="your OTP for Verification of Registration",
            message=f"Your OTP is {otp}. It is valid for 10 minutes.",
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            recipient_list=[email],
            fail_silently=False,   
        )
        return otp
    except Exception as e:
        return False, f"Failed to send OTP: {e}"
    
def store_temp_user_data(email, data, otp):
    """
    Store temporary user data in cashe with OTP expiry time.
    """

    cache.set(
        f"temp_user_data_{email}",
        {
            "data": data,
            "otp" : otp,
            "otp_attempts": 0,
            "otp_expiry": timezone.now() + timezone.timedelta(seconds=OTP_EXPIRY_SECONDS),
        }
    )

# API VIEWS

class RegisterUserView(APIView):
    """
    API View to register a new user via OTP and real-time email verification.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            full_name = serializer.validated_data['full_name']
            phone_number = serializer.validated_data['phone_number']

            # 1. Validate email with mailboxlayer API
            is_valid_email = validate_email_with_mailboxlayer(email)
            if not is_valid_email:
                return Response({"error": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 2. Generate and send OTP 
            otp = generate_and_send_otp(email)
            if not otp:
                return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # 3. Store temporary user data in cache with OTP expiry time
            store_temp_user_data(email, serializer.validated_data, otp)

            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOTPView(APIView):
    """
    API View to verify OTP and create a new user 
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp_input = request.data.get("otp")

        cached = cache.get(f"temp_user_data_{email}")
        if not cached:
            return Response({"error": "OTP expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check OTP
        if cached["otp"] != otp_input:
            cached["otp_attempts"] += 1
            cache.set(f"temp_user_data_{email}", cached, timeout=OTP_EXPIRY_SECONDS)
            
            if cached["otp_attempts"] >= MAX_OTP_ATTEMPTS:
                cache.delete(f"temp_user_data_{email}")
                return Response(
                    {"error": "Maximum OTP attempts exceeded. Please register again."},
                    status=status.HTTP_403_FORBIDDEN
                )

            cache.set(f"temp_user_data_{email}", cached, timeout=OTP_EXPIRY_SECONDS)
            return Response(
                {"error": f"Invalid OTP. Attempt {cached['otp_attempts']}/{MAX_OTP_ATTEMPTS}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If OTP is matched, create user and delete temporary data
        user_data = cached["data"]
        serializer = RegisterUserSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            cache.delete(f"temp_user_data_{email}")
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
        Login API View for user login and token generation.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']  # Get the validated user directly
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
        API View for logging out a user and invalidating their refresh token.
    """

    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the refresh token ti invalidate token
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "sucessfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": f"Error logging out: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")

        try:
            user = get_user_model().objects.get(email=email)
            token = generate_reset_token(user.id)
            return Response({"reset_token": token}, status=200)

        except get_user_model().DoesNotExist:
            return Response({"message": "If an account with that email exists, you will receive a reset token."}, status=200)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        user_id = decode_reset_token(token)

        if user_id =='expired' :
            return Response({'error': "Token has expired. Please request a new reset token."}, status=status.HTTP_400_BAD_REQUEST)
        elif user_id is None:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        try: 
            user = get_user_model().objects.get(id=user_id)

            # update the user's password
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
