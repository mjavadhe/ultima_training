# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('process/<uuid:enrollment_id>/', views.payment_process, name='payment_process'),
    path('iranian/<uuid:payment_id>/complete/', views.iranian_payment_complete, name='iranian_payment_complete'),
    path('webhooks/paypal/', views.paypal_webhook, name='paypal_webhook'),
]