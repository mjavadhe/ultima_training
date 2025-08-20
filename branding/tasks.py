# branding/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_contact_notification(form_data):
    try:
        subject = f'New Contact Form Submission - {form_data["purpose"]}'
        message = f"""
        New contact form submission:
        
        Name: {form_data['name']}
        Email: {form_data['email']}
        Company: {form_data.get('company', 'N/A')}
        Purpose: {form_data['purpose']}
        
        Message:
        {form_data['message']}
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )
    except Exception as e:
        logger.exception(f"Error sending contact notification: {e}")

@shared_task
def send_speaking_request_notification(form_data):
    try:
        subject = f'New Speaking Request - {form_data["event_type"]}'
        message = f"""
        New speaking engagement request:
        
        Name: {form_data['name']}
        Email: {form_data['email']}
        Company: {form_data['company']}
        Event Type: {form_data['event_type']}
        Event Date: {form_data['event_date']}
        Audience Size: {form_data['audience_size']}
        Location: {form_data['location']}
        Budget Range: {form_data['budget_range']}
        
        Topics:
        {form_data['topics']}
        
        Additional Requirements:
        {form_data.get('additional_requirements', 'None')}
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )
    except Exception as e:
        logger.exception(f"Error sending speaking request notification: {e}")