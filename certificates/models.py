# certificates/models.py
from django.db import models
from courses.models import Enrollment
import uuid

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    
    certificate_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    
    # QR Code data
    qr_data = models.JSONField()
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    # Certificate file
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    is_valid = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Certificate {self.certificate_number}"
    
    def generate_certificate_number(self):
        import random
        import string
        return 'CERT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
