from django.urls import path

from profiles.views import *

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('set_gmail/', ChangeGoogeAccountView.as_view(), name='set_gmail'),
    path('set_email/', SetEmailView.as_view(), name='set_email'),
    path('set_password/', SetPasswordView.as_view(), name='set_password'),
]
