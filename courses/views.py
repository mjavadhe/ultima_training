# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
import json

from .models import Course, CourseSession, Enrollment, Feedback
from .forms import CourseRegistrationForm, FeedbackForm
from payments.models import Payment

def course_list(request):
    courses = Course.objects.filter(is_active=True).prefetch_related('sessions')
    
    # Filters
    course_type = request.GET.get('type')
    if course_type:
        courses = courses.filter(course_type=course_type)
    
    search = request.GET.get('search')
    if search:
        courses = courses.filter(
            Q(name__icontains=search) | Q(short_description__icontains=search)
        )
    
    context = {'courses': courses}
    return render(request, 'courses/course_list.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    upcoming_sessions = course.sessions.filter(
        start_datetime__gte=timezone.now(),
        is_active=True
    ).order_by('start_datetime')
    
    context = {
        'course': course,
        'upcoming_sessions': upcoming_sessions,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def course_register(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST, course=course)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user
            enrollment.course = course
            enrollment.tracking_number = enrollment.generate_tracking_number()
            enrollment.save()
            
            # Redirect to payment
            return redirect('payment_process', enrollment_id=enrollment.id)
    else:
        form = CourseRegistrationForm(course=course)
    
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'courses/course_register.html', context)

@login_required
def submit_feedback(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        student=request.user,
        status='completed'
    )
    
    try:
        feedback = enrollment.feedback
    except Feedback.DoesNotExist:
        feedback = None
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.enrollment = enrollment
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('student_dashboard')
    else:
        form = FeedbackForm(instance=feedback)
    
    context = {
        'enrollment': enrollment,
        'form': form,
    }
    return render(request, 'courses/submit_feedback.html', context)

@login_required
def cancel_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        student=request.user,
        status__in=['pending', 'enrolled']
    )
    
    # Check if cancellation is allowed (before course start)
    if enrollment.session.start_datetime <= timezone.now():
        messages.error(request, 'Cancellation not allowed - course has started.')
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        # Process cancellation
        from payments.forms import RefundRequestForm
        form = RefundRequestForm(request.POST, payment=enrollment.payment)
        if form.is_valid():
            refund = form.save(commit=False)
            refund.payment = enrollment.payment
            refund.save()
            
            enrollment.status = 'cancelled'
            enrollment.save()
            
            # Send cancellation email
            from .tasks import send_cancellation_email
            send_cancellation_email.delay(enrollment.id, refund.id)
            
            messages.success(request, 'Cancellation request submitted successfully!')
            return redirect('student_dashboard')
    else:
        from payments.forms import RefundRequestForm
        form = RefundRequestForm(payment=enrollment.payment)
    
    context = {
        'enrollment': enrollment,
        'form': form,
    }
    return render(request, 'courses/cancel_enrollment.html', context)

# Instructor Views
@login_required
def instructor_approve_student(request, enrollment_id):
    if request.user.user_type != 'instructor':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        course__instructor=request.user,
        status='pending'
    )
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            enrollment.status = 'enrolled'
            enrollment.approved_by = request.user
            enrollment.approval_date = timezone.now()
            enrollment.save()
            
            # Send approval email
            from .tasks import send_approval_email
            send_approval_email.delay(enrollment.id)
            
            return JsonResponse({'status': 'success', 'message': 'Student approved'})
        
        elif action == 'reject':
            reason = request.POST.get('reason', '')
            enrollment.status = 'rejected'
            enrollment.rejection_reason = reason
            enrollment.save()
            
            # Send rejection email
            from .tasks import send_rejection_email
            send_rejection_email.delay(enrollment.id)
            
            return JsonResponse({'status': 'success', 'message': 'Student rejected'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def instructor_review_feedback(request, feedback_id):
    if request.user.user_type != 'instructor':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    feedback = get_object_or_404(
        Feedback,
        id=feedback_id,
        enrollment__course__instructor=request.user
    )
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            feedback.is_approved = True
            feedback.reviewed_by = request.user
            feedback.review_date = timezone.now()
            feedback.save()
            
            # Generate certificate
            from certificates.tasks import generate_certificate
            generate_certificate.delay(feedback.enrollment.id)
            
            return JsonResponse({'status': 'success', 'message': 'Feedback approved'})
        
        elif action == 'request_changes':
            comments = request.POST.get('comments', '')
            feedback.review_comments = comments
            feedback.save()
            
            # Send revision request email
            from .tasks import send_revision_request_email
            send_revision_request_email.delay(feedback.id)
            
            return JsonResponse({'status': 'success', 'message': 'Revision requested'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)