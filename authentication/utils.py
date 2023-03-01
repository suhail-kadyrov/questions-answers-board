import threading
import time

import face_recognition
from django.conf import settings
from django.contrib.auth import authenticate, tokens
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from google.auth.transport import requests
from google.oauth2 import id_token
from PIL import Image, ImageDraw
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import CustomUser, LoginAttempt


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to']]
        )
        EmailThread(email).start()


class Verification:
    @staticmethod
    def send_email(user, request):
        token = RefreshToken.for_user(user).access_token

        doamin = get_current_site(request).domain

        path = reverse('verify')
        url = 'http://{}{}?token={}'.format(doamin, path, token)

        body = 'Hi, {}! Click on the link below to activate your account on "Questions & answers board":\n{}\nThis link will expire in an hour. After that, you will not be able to access your account at all.'.format(user.full_name, url)
        data = {
            'subject': 'Verify your email',
            'body': body,
            'to': user.email
        }

        Email.send(data)


class PasswordReset:
    @staticmethod
    def send_email(user, request):
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = tokens.PasswordResetTokenGenerator().make_token(user)

        doamin = get_current_site(request).domain

        path = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        redirect_url = settings.FRONTEND_URL + '/reset-password-complete'
        url = 'http://{}{}?redirect_url={}'.format(doamin, path, redirect_url)

        body = 'Hi! You can use the link below to reset your password on "Questions & answers board":\n{}'.format(url)
        data = {
            'subject': 'Reset your password',
            'body': body,
            'to': user.email
        }

        Email.send(data)


class Google:
    @staticmethod
    def validate(token):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        except:
            return "The token is either invalid or has expired"

    @staticmethod
    def authenticate(provider, user_id, email, name, capture=None):
        user = CustomUser.objects.filter(email=email)
        if user.exists():
            if provider == user[0].auth_provider:
                authenticated_user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
            else:
                raise AuthenticationFailed(detail='Please continue your login using ' + user[0].auth_provider)
        else:
            user = CustomUser.objects.create_user(
                email=email,
                full_name=name,
                role='STUDENT',
                is_verified=True,
                auth_provider=provider,
                password=settings.SOCIAL_AUTH_PASSWORD
            )
            authenticated_user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)

        if authenticated_user.image:
                image = authenticated_user.image.url
        else:
                image = None
        
        LoginAttempt.objects.create(
            user=authenticated_user,
            capture=capture
        )
        
        return {
            'id': authenticated_user.id,
            'email': authenticated_user.email,
            'auth_provider': authenticated_user.auth_provider,
            'full_name': authenticated_user.full_name,
            'role': authenticated_user.role,
            'image': image,
            'tokens': authenticated_user.tokens()
        }


class FaceRecognition:
    @staticmethod
    def compare_face(img1_path,img2_path):
        img_1 = face_recognition.load_image_file(img1_path)
        img1_encoding = face_recognition.face_encodings(img_1)[0]

        img_2 = face_recognition.load_image_file(img2_path)
        img2_encoding = face_recognition.face_encodings(img_2)[0]
        
        result = face_recognition.compare_faces([img1_encoding],img2_encoding)
        return result
