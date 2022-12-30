from rest_framework import serializers
from authentication.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'role', 'image']
    

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