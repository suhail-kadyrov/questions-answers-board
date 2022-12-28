from django.urls import path
from authentication.views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', EmailVerifyView.as_view(), name='verify'),
]
