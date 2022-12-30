from authentication.models import CustomUser
from authentication.utils import Verification
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from profiles.permissions import VerifiedUser

from profiles.serializers import *


class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, VerifiedUser]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.image = serializer.validated_data.get('image')
        request.user.full_name = serializer.validated_data.get('full_name')
        request.user.save()
        return Response({})


class SetEmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated, VerifiedUser]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(serializer.data['password']):
            if request.user.email != serializer.data['email'] and not CustomUser.objects.filter(email=serializer.data['email']).exists():
                request.user.is_verified = False
                request.user.email = serializer.data['email']
                Verification.send_email(request.user, request)
                request.user.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        return Response({'error': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordView(generics.GenericAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated, VerifiedUser]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(serializer.data['old_password']):
            request.user.set_password(serializer.data['new_password'])
            request.user.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        return Response({'error': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
