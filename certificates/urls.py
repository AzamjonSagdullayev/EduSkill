from django.urls import path
from certificates import views

app_name = 'certificates'

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('<int:certificate_id>/', views.certificate_detail, name='certificate_detail'),
]
