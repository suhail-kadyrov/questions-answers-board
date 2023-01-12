from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', EmailVerifyView.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset_password/', PasswordResetView.as_view(), name ='reset_password'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
    path('google/', GoogleAuthView.as_view(), name ='google_auth')
]
