import threading

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken

# class EmailThread(threading.Thread):
#     def __init__(self, email):
#         self.email = email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()


class Email:
    @staticmethod
    def send(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to']]
        )
        email.send()


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
        token = PasswordResetTokenGenerator().make_token(user)

        doamin = get_current_site(request).domain

        path = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        redirect_url = request.data.get('redirect_url', '')
        url = 'http://{}{}?redirect_url={}'.format(doamin, path, redirect_url)

        body = 'Hi! You can use the link below to reset your password on "Questions & answers board":\n{}'.format(url)
        data = {
            'subject': 'Reset your password',
            'body': body,
            'to': user.email
        }

        Email.send(data)
