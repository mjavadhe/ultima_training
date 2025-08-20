from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'enrollment', 'issue_date', 'is_valid')
    search_fields = ('certificate_number',)