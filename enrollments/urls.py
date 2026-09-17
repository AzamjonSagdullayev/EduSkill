from django.urls import path
from enrollments import views

app_name = 'enrollments'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('courses/<slug:course_slug>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<slug:course_slug>/lessons/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
]
