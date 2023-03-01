from authentication.models import CustomUser
from authentication.utils import Google, Verification
from django.conf import settings
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiles.permissions import IsVerifiedUser
from profiles.serializers import *


class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.full_name = serializer.validated_data.get('full_name')
        request.user.save()
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.image = serializer.validated_data.get('image')
        request.user.save()
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)

    
class SetEmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]

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


class SetFaceView(generics.GenericAPIView):
    serializer_class = FaceSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.face = serializer.validated_data.get('face')
        request.user.save()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class ChangeGoogeAccountView(views.APIView):
    def put(self, request):
        id_token = request.data.get('id_token')
        user_data = Google.validate(id_token)
        try:
            user_data['sub']
        except:
            return Response({'error': 'The token is invalid or expired. Please login again.'}, status=status.HTTP_401_UNAUTHORIZED)

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            return Response({'error': 'oops, who are you?'}, status=status.HTTP_401_UNAUTHORIZED)
        
        email = user_data['email']

        if CustomUser.objects.exclude(email=request.user.email).filter(email=email).exists():
            return Response({'detail': 'This email has already taken'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.user.email = email
            request.user.save()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class SetPasswordView(generics.GenericAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(serializer.data['old_password']):
            request.user.set_password(serializer.data['new_password'])
            request.user.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        return Response({'error': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
