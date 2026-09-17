from django.urls import path
from quizzes import views

app_name = 'quizzes'

urlpatterns = [
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('result/<int:result_id>/', views.quiz_result, name='quiz_result'),
]
