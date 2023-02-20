from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.managers import CustomUserManager

USER_ROLE_CHOICES = (
    ('ADMIN', 'ADMIN'),
    ('PROFESSOR', 'PROFESSOR'),
    ('STUDENT', 'STUDENT'),
)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("Email"), unique=True)
    full_name = models.CharField(max_length=64)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='STUDENT')
    is_verified = models.BooleanField(default=False)
    image = CloudinaryField('image', null=True, blank=True, folder='q-a-board-users/')
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default='email')
    face = CloudinaryField('face', null=True, blank=True, folder='q-a-board-users/faces/')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
