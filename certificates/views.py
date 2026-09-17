from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from certificates.models import Certificate


@login_required
def certificate_list(request):
    certificates = Certificate.objects.filter(
        user=request.user
    ).select_related('course')
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})


@login_required
def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(
        Certificate,
        pk=certificate_id,
        user=request.user  # Faqat o'z sertifikatini ko'ra oladi
    )
    return render(request, 'certificates/certificate_detail.html', {'certificate': certificate})
