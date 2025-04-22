from django.urls import path
from .views import RegisterUserView, VerifyOTPView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
]
