# courses/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_approval_email(enrollment_id):
    from .models import Enrollment
    
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
        
        subject = f'Course Enrollment Approved - {enrollment.course.name}'
        html_message = render_to_string('emails/enrollment_approved.html', {
            'enrollment': enrollment,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [enrollment.student.email],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Error sending approval email: {e}")

@shared_task
def send_rejection_email(enrollment_id):
    from .models import Enrollment
    
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
        
        subject = f'Course Enrollment Update - {enrollment.course.name}'
        html_message = render_to_string('emails/enrollment_rejected.html', {
            'enrollment': enrollment,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [enrollment.student.email],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Error sending rejection email: {e}")

@shared_task
def send_cancellation_email(enrollment_id, refund_id):
    from .models import Enrollment
    from payments.models import Refund
    
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
        refund = Refund.objects.get(id=refund_id)
        
        subject = f'Cancellation Confirmed - {enrollment.course.name}'
        html_message = render_to_string('emails/cancellation_confirmed.html', {
            'enrollment': enrollment,
            'refund': refund,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [enrollment.student.email],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Error sending cancellation email: {e}")

@shared_task
def send_revision_request_email(feedback_id):
    from .models import Feedback
    
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        
        subject = f'Feedback Revision Request - {feedback.enrollment.course.name}'
        html_message = render_to_string('emails/feedback_revision.html', {
            'feedback': feedback,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [feedback.enrollment.student.email],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Error sending revision request email: {e}")
