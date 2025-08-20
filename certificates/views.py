
# certificates/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.conf import settings
import os

from .models import Certificate

@login_required
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(
        Certificate,
        id=certificate_id,
        enrollment__student=request.user,
        is_valid=True
    )
    
    if not certificate.certificate_file:
        raise Http404("Certificate file not found")
    
    file_path = certificate.certificate_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.certificate_number}.pdf"'
            return response
    
    raise Http404("Certificate file not found")

def verify_certificate(request, certificate_number):
    """Public certificate verification"""
    try:
        certificate = Certificate.objects.get(
            certificate_number=certificate_number,
            is_valid=True
        )
        context = {
            'certificate': certificate,
            'is_valid': True,
        }
    except Certificate.DoesNotExist:
        context = {
            'is_valid': False,
            'error': 'Certificate not found or invalid'
        }
    
    return render(request, 'certificates/verify.html', context)
