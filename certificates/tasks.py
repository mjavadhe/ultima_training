# certificates/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import qrcode
from io import BytesIO
from django.core.files import File
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

@shared_task
def generate_certificate(enrollment_id):
    from courses.models import Enrollment
    from .models import Certificate
    
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
        
        # Generate certificate
        certificate = Certificate.objects.create(
            enrollment=enrollment,
            certificate_number=Certificate().generate_certificate_number(),
            qr_data={
                'student_name': enrollment.student.get_full_name(),
                'course_name': enrollment.course.name,
                'completion_date': enrollment.completion_date.isoformat() if enrollment.completion_date else None,
                'certificate_number': certificate.certificate_number,
                'mobile': enrollment.student.mobile,
            }
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(str(certificate.qr_data))
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        certificate.qr_code_image.save(
            f'qr_{certificate.certificate_number}.png',
            File(qr_buffer),
            save=False
        )
        
        # Generate PDF certificate
        pdf_buffer = BytesIO()
        p = canvas.Canvas(pdf_buffer, pagesize=letter)
        
        # Certificate design
        width, height = letter
        
        # Title
        p.setFont("Helvetica-Bold", 24)
        p.drawCentredText(width/2, height-100, "CERTIFICATE OF COMPLETION")
        
        # Ultima Training logo area
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredText(width/2, height-140, "ULTIMA TRAINING")
        
        # Student name
        p.setFont("Helvetica-Bold", 18)
        p.drawCentredText(width/2, height-200, f"This certifies that")
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredText(width/2, height-230, enrollment.student.get_full_name())
        
        # Course info
        p.setFont("Helvetica", 14)
        p.drawCentredText(width/2, height-270, f"has successfully completed the course")
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredText(width/2, height-300, enrollment.course.name)
        
        # Date and location
        p.setFont("Helvetica", 12)
        completion_date = enrollment.completion_date.strftime('%B %d, %Y') if enrollment.completion_date else 'N/A'
        p.drawCentredText(width/2, height-340, f"Completed on: {completion_date}")
        p.drawCentredText(width/2, height-360, f"Location: {enrollment.session.location}")
        
        # Certificate number
        p.drawCentredText(width/2, height-400, f"Certificate Number: {certificate.certificate_number}")
        
        # Signatures
        p.setFont("Helvetica", 10)
        p.drawString(100, 150, "Dr. Josef Balahan")
        p.drawString(100, 130, "Founder & Lead Trainer")
        
        p.drawString(400, 150, enrollment.course.instructor.get_full_name())
        p.drawString(400, 130, "Course Instructor")
        
        # QR Code (placeholder - in real implementation, you'd embed the actual QR image)
        p.drawString(width-150, 100, "QR Code")
        p.rect(width-150, 120, 100, 100, stroke=1, fill=0)
        
        p.save()
        pdf_buffer.seek(0)
        
        certificate.certificate_file.save(
            f'certificate_{certificate.certificate_number}.pdf',
            File(pdf_buffer),
            save=True
        )
        
        # Send certificate email
        send_certificate_email.delay(certificate.id)
        
    except Exception as e:
        print(f"Error generating certificate: {e}")

@shared_task
def send_certificate_email(certificate_id):
    from .models import Certificate
    
    try:
        certificate = Certificate.objects.get(id=certificate_id)
        
        subject = f'Your Certificate is Ready - {certificate.enrollment.course.name}'
        html_message = render_to_string('emails/certificate_ready.html', {
            'certificate': certificate,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [certificate.enrollment.student.email],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Error sending certificate email: {e}")
