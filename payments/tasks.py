# payments/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_payment_confirmation_email(payment_id):
    from .models import Payment
    
    try:
        payment = Payment.objects.get(id=payment_id)
        
        subject = f'Payment Confirmation - {payment.enrollment.course.name}'
        html_message = render_to_string('emails/payment_confirmation.html', {
            'payment': payment,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [payment.enrollment.student.email],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Error sending payment confirmation email: {e}")
