from django.urls import path
from .views import RegisterView, CustomLoginView, PasswordResetView, VerifyEmailView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
