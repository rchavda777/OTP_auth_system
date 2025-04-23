import os
import jwt
from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta

load_dotenv()
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Expiry time for the reset token 15 minutes
TOKEN_EXPIRATION_TIME = timedelta(minutes=15)

def generate_reset_token(user_id):
    """
    Generate a JWT token for password reset.
    The token will include the user_id and an expiration time.
    """
    payload  = {
        'user_id': user_id,
        'exp': timezone.now() + TOKEN_EXPIRATION_TIME,
        'iat': timezone.now()  # Issued at time
    }

    # Generate JWT token using HS256 algorithm
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_reset_token(token):
    """
    Decode the JWT token and return the user_id.
    If token is invalid or expired, return None or 'expired' as applicable.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'expired'
    except jwt.InvalidTokenError:
        None

