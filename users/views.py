import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterUserSerializer
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

class RegisterUserView(APIView):
    """
    API view to register a new user.
    """
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            # Real-time email validation using mailboxlayer API
            email = serializer.validated_data['email']
            api_key = os.getenv('MAILBOXLAYER_API_KEY')

            email_validation_url = f"http://apilayer.net/api/check?access_key={api_key}&email={email}&smtp=1&format=1"
            validation_response = requests.get(email_validation_url).json()

            if not validation_response.get('smtp_check', False):
                return Response({"error": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({"message": "user registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)