from datetime import datetime, timedelta

from chat.models import *
from django.shortcuts import get_object_or_404
from profiles.permissions import IsVerifiedUser
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


# Create your views here.
class NotificationListView(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    displayed_notifications_limit = 30

    def get(self, request):
        serializer = self.serializer_class(data=self.get_queryset(), many=True)
        serializer.is_valid()

        # Getting rid of expired notifications
        Notification.objects.filter(
            receiver=request.user,
            is_seen=True,
            sent_at__lte=datetime.now() - timedelta(days=90)
        ).delete()

        return Response(serializer.data)
    
    def get_queryset(self):
        notifications = Notification.objects.filter(receiver=self.request.user)
        not_seen = notifications.filter(is_seen=False)
        if not_seen.count() >= self.displayed_notifications_limit:
            return not_seen.order_by('-sent_at')
        seen = notifications.order_by('is_seen', '-sent_at')
        return seen[:self.displayed_notifications_limit]


class NotificationSeenView(views.APIView):
    def patch(self, request, pk):
        notification = get_object_or_404(Notification, id=pk)
        notification.is_seen = True
        notification.save()
        return Response({'is_seen': True})


class StudentEnrollmentSentView(views.APIView):
    def post(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        Notification.objects.get_or_create(
            name='PROFESSOR_ENROLMENT_REQUEST',
            text=f'{request.user.full_name} wants to enroll to {course.name}',
            receiver=course.professor,
            user=request.user,
            course=course,
        )
        Notification.objects.get_or_create(
            name='STUDENT_REQUEST_SENT',
            text=f'Your request for enrollment to {course.name} has sent',
            receiver=request.user,
            course=course,
        )
        return Response({'message': 'success'})


class StudentEnrollmentAnswerView(views.APIView):
    def put(self, request):
        student = get_object_or_404(CustomUser, id=request.data.get('user'))
        course = get_object_or_404(Course, id=request.data.get('course'))
        course.students.add(student)
        course.save()
        Notification.objects.create(
            name='STUDENT_REQUEST_ACCEPTED',
            text=f'Your request for enrollment to {course.name} has accepted',
            receiver=student,
            course=course,
        )
        Notification.objects.create(
            name='ADMIN_NEW_ENROLMENT',
            text=f'{student.full_name} has enrolled to {course.name}',
            receiver=CustomUser.objects.get(role='ADMIN'),
            user=student,
            course=course
        )
        return Response({'message': 'success'})
    
    def patch(self, request):
        student = get_object_or_404(CustomUser, id=request.data.get('user'))
        course = get_object_or_404(Course, id=request.data.get('course'))
        Notification.objects.create(
            name='STUDENT_REQUEST_REJECTED',
            text=f'Your request for enrollment to {course.name} has rejected',
            receiver=student,
            course=course,
        )
        return Response({'message': 'success'})


class ProfessorPromotionSentView(views.APIView):
    def post(self, request):
        Notification.objects.get_or_create(
            name='ADMIN_PROMOTION_REQUEST',
            text=f'{request.user.full_name} wants to become a professor',
            receiver=CustomUser.objects.get(role='ADMIN'),
            user=request.user,
        )
        Notification.objects.get_or_create(
            name='PROFESSOR_PROMOTION_SENT',
            text='Your request for for becoming a professor has sent',
            receiver=request.user,
        )
        return Response({'message': 'success'})


class ProfessorPromotionAnswerView(views.APIView):
    def put(self, request):
        student = get_object_or_404(CustomUser, id=request.data.get('user'))
        student.role = 'PROFESSOR'
        student.save()
        Notification.objects.create(
            name='PROFESSOR_PROMOTION_ACCEPTED',
            text=f'Your request for for becoming a professor has accepted',
            receiver=student,
        )
        return Response({'message': 'success'})
    
    def patch(self, request):
        student = get_object_or_404(CustomUser, id=request.data.get('user'))
        Notification.objects.create(
            name='PROFESSOR_PROMOTION_REJECTED',
            text=f'Your request for for becoming a professor has rejected',
            receiver=student,
        )
        return Response({'message': 'success'})
