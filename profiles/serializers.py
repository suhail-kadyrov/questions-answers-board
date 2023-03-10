from authentication.models import CustomUser
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    auth_provider = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    image = serializers.ImageField(allow_empty_file=True, use_url=True, read_only=True)
    face = serializers.ImageField(allow_empty_file=True, use_url=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'auth_provider', 'full_name', 'role', 'image', 'face']


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, use_url=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['image']


class FaceSerializer(serializers.ModelSerializer):
    face = serializers.ImageField(allow_empty_file=True, use_url=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['face']


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=1, max_length=32)
    new_password = serializers.CharField(min_length=8, max_length=32)

    class Meta:
        fields = ['old_password', 'new_password']


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=1, max_length=32)

    class Meta:
        fields = ['email', 'password']
