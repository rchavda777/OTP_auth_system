from django.urls import path
from .views import RegisterUserView, VerifyOTPView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
