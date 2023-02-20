import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from authentication.models import CustomUser
from authentication.serializers import *
from authentication.utils import PasswordReset, Verification


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])

        Verification.send_email(user, request)
        
        return Response(user_data, status=status.HTTP_201_CREATED)


class EmailVerifyView(views.APIView):
     def get(self, request):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = CustomUser.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            return HttpResponsePermanentRedirect(settings.FRONTEND_URL + '/verified?error=Expired%20link')
        except jwt.exceptions.DecodeError:
            return HttpResponsePermanentRedirect(settings.FRONTEND_URL + '/verified?error=Invalid%20token')
        except CustomUser.DoesNotExist:
            return HttpResponsePermanentRedirect(settings.FRONTEND_URL + '/verified?error=User%20is%20not%20found')
        else:
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return HttpResponsePermanentRedirect(settings.FRONTEND_URL + '/verified')


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            PasswordReset.send_email(user, request)

        return Response({'success': 'A link to reset your password has been sent to your email.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(views.APIView):
    def get(self, request, uidb64, token):

        redirect_url = request.query_params.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if redirect_url:
                    return HttpResponsePermanentRedirect(redirect_url)
            else:
                if redirect_url:
                    return HttpResponsePermanentRedirect(redirect_url+'?uidb64='+uidb64+'&token='+token)
        except DjangoUnicodeDecodeError:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return HttpResponsePermanentRedirect(redirect_url)
            except UnboundLocalError as e:
                return HttpResponsePermanentRedirect(redirect_url)


class PasswordResetCompleteView(generics.GenericAPIView):
    serializer_class = PasswordResetCompleteSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GoogleAuthView(generics.GenericAPIView):
    serializer_class = GoogleSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data['id_token'], status=status.HTTP_200_OK)
    
    



class FaceAuthView(generics.GenericAPIView):
    serializer_class = FaceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)