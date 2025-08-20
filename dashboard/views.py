# dashboard/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone

from courses.models import Enrollment, Course
from certificates.models import Certificate

@login_required
def student_dashboard(request):
    user = request.user
    
    # Registered courses (pending and enrolled)
    registered_enrollments = Enrollment.objects.filter(
        student=user,
        status__in=['pending', 'enrolled'],
        session__start_datetime__gte=timezone.now()
    ).select_related('course', 'session').prefetch_related('certificate')
    
    # Pending feedback courses
    pending_feedback = Enrollment.objects.filter(
        student=user,
        status='completed',
        feedback__isnull=True
    ).select_related('course', 'session').prefetch_related('certificate')
    
    # Completed courses with certificates
    completed_enrollments = Enrollment.objects.filter(
        student=user,
        status='completed',
        feedback__isnull=False,
        feedback__is_approved=True
    ).select_related('course', 'session').prefetch_related('certificate')
    
    context = {
        'registered_enrollments': registered_enrollments,
        'pending_feedback': pending_feedback,
        'completed_enrollments': completed_enrollments,
    }
    
    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def instructor_dashboard(request):
    if request.user.user_type != 'instructor':
        messages.error(request, 'Access denied.')
        return redirect('student_dashboard')
    
    # Instructor's courses
    courses = Course.objects.filter(
        Q(instructor=request.user) | Q(co_instructor=request.user)
    )
    
    # Pending approvals
    pending_approvals = Enrollment.objects.filter(
        course__in=courses,
        status='pending'
    ).select_related('student', 'course', 'session')
    
    # Pending feedback reviews
    pending_reviews = Enrollment.objects.filter(
        course__in=courses,
        feedback__is_approved=False,
        feedback__isnull=False
    ).select_related('feedback', 'course')
    
    context = {
        'courses': courses,
        'pending_approvals': pending_approvals,
        'pending_reviews': pending_reviews,
    }
    return render(request, 'dashboard/instructor_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('student_dashboard')
    
    # Admin stats
    user_count = User.objects.count()
    enrollment_count = Enrollment.objects.count()
    
    context = {
        'user_count': user_count,
        'enrollment_count': enrollment_count,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)