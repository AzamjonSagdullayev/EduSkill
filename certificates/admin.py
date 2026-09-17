from django.contrib import admin
from certificates.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'certificate_number', 'issued_at']
    list_filter = ['issued_at', 'course']
    search_fields = ['user__username', 'course__title', 'certificate_number']
    ordering = ['-issued_at']
    readonly_fields = ['certificate_number', 'issued_at']
