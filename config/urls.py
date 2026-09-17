from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('enrollments.urls', namespace='enrollments')),
    path('quizzes/', include('quizzes.urls', namespace='quizzes')),
    path('certificates/', include('certificates.urls', namespace='certificates')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'config.views.handler404'
handler403 = 'config.views.handler403'
handler500 = 'config.views.handler500'
