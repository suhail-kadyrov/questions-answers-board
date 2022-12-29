from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from authentication.models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=32, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'role', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=32, min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=64, min_length=1, read_only=True)
    role = serializers.CharField(max_length=10, min_length=5, read_only=True)
    image = serializers.CharField(read_only=True)
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
        fields = ['id', 'email', 'full_name', 'role', 'image', 'password', 'tokens']

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

        return {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role,
            'image': user.image,
            'tokens': user.tokens
        }


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, write_only=True)

    class Meta:
        fields = ['email', 'redirect_url']


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
