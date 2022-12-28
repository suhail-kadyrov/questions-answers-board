from authentication.models import CustomUser
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=32, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)