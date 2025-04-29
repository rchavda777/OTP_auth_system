from django.urls import path
from users.views import RegisterUserView, VerifyOTPView, LoginView, LogoutView
from users.views import UserProfileAPIView, ResetPasswordView, ForgotPasswordView
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password')
]
