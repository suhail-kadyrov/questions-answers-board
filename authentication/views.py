from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import CustomUser
from authentication.serializers import SignUpSerializer
from authentication.utils import Email


class SignUpView(generics.GenericAPIView):

    serializer_class = SignUpSerializer
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        doamin = get_current_site(request).domain

        path = reverse('verify')
        url = 'http://{}{}?token={}'.format(doamin, path, token)

        body = 'Hi, {}! Click on the link below to activate your account on "Questions & answers board":\n\n{}'.format(user.full_name, url)
        data = {
            'subject': 'Verify your email',
            'body': body,
            'to': user.email
        }

        Email.send(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class EmailVerifyView(views.APIView):
    def get(self, request):
        pass