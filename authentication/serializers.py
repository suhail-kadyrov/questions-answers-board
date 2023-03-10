import urllib
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from authentication.models import CustomUser, LoginAttempt
from authentication.utils import Google, FaceRecognition


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=32, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'role', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    auth_provider = serializers.CharField(max_length=6, min_length=5, read_only=True)
    password = serializers.CharField(max_length=32, min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=64, min_length=1, read_only=True)
    role = serializers.CharField(max_length=10, min_length=5, read_only=True)
    image = serializers.ImageField(allow_empty_file=True, use_url=True, read_only=True)
    capture = serializers.ImageField(allow_empty_file=True, use_url=True, required=False)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])
        tokens = user.tokens()
        return {
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'auth_provider', 'full_name', 'role', 'image', 'capture', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        LoginAttempt.objects.create(
            user=user,
            capture=attrs.get('capture')
        )

        return {
            'id': user.id,
            'email': user.email,
            'auth_provider': user.auth_provider,
            'full_name': user.full_name,
            'role': user.role,
            'image': user.image,
            'tokens': user.tokens
        }


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email',]


class PasswordResetCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Invalid link', 401)

            user.set_password(password)
            user.save()

            return user
        except Exception:
            raise AuthenticationFailed('Invalid link', 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class GoogleSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def validate(self, attrs):
        id_token = attrs.get('id_token')
        user_data = Google.validate(id_token)

        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return Google.authenticate(provider=provider, user_id=user_id, email=email, name=name, capture=attrs.get('capture'))


class FaceSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    face = serializers.ImageField(allow_empty_file=True, use_url=True)
    
    auth_provider = serializers.CharField(max_length=6, min_length=5, read_only=True)
    full_name = serializers.CharField(max_length=64, min_length=1, read_only=True)
    role = serializers.CharField(max_length=10, min_length=5, read_only=True)
    image = serializers.ImageField(allow_empty_file=True, use_url=True, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])
        tokens = user.tokens()
        return {
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }

    class Meta:
        fields = ['id', 'email', 'auth_provider', 'full_name', 'role', 'image', 'face', 'tokens']
    
    def validate(self,attrs):
        user_email = attrs.get('email')
        user_image = attrs.get('face')
        users = CustomUser.objects.filter(email = user_email)
        if users.exists():
            user = users.first()
            user_face = user.face
            if user_face is None:
                raise AuthenticationFailed('Face is not registered')
            face = urllib.request.urlopen(user_face.url)
            result = FaceRecognition.compare_face(face, user_image)
            if result[0]:
                if not user.is_active:
                    raise AuthenticationFailed('Account disabled')
                if not user.is_verified:
                    raise AuthenticationFailed('Email is not verified')
                LoginAttempt.objects.create(
                    user=user,
                    capture=user_image
                )
                return {
                    'id': user.id,
                    'email': user.email,
                    'auth_provider': user.auth_provider,
                    'full_name': user.full_name,
                    'role': user.role,
                    'image': user.image,
                    'face': user.face,
                    'tokens': user.tokens
                }
            raise AuthenticationFailed('Face does not match')
        raise AuthenticationFailed('Invalid Creadentials')
    