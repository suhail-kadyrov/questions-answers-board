from django.urls import path

from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notifications_list"),
    path("seen/<int:pk>/", views.NotificationSeenView.as_view(), name="notifications_seen"),
    path("student/enrollment/<int:pk>/sent/", views.StudentEnrollmentSentView.as_view()),
    path("student/enroll/answer/", views.StudentEnrollmentAnswerView.as_view()),
    path("professor/promotion/sent/", views.ProfessorPromotionSentView.as_view()),
    path("professor/promotion/answer/", views.ProfessorPromotionAnswerView.as_view()),
]
