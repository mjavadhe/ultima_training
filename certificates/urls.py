# certificates/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('download/<uuid:certificate_id>/', views.download_certificate, name='download_certificate'),
    path('verify/<str:certificate_number>/', views.verify_certificate, name='verify_certificate'),
]