# Ultima Training Platform - Complete Django Implementation

# requirements.txt
"""
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
Pillow==10.0.1
django-crispy-forms==2.0
crispy-bootstrap5==0.7
django-allauth==0.57.0
celery==5.3.4
redis==5.0.1
reportlab==4.0.7
qrcode==7.4.2
python-decouple==3.8
stripe==7.8.0
paypal-checkout-serversdk==1.0.1
django-storages==1.14.2
boto3==1.34.0
whitenoise==6.6.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
"""

# settings.py
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Local apps
    'accounts',
    'courses',
    'payments',
    'certificates',
    'branding',
    'dashboard',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ultima_training.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='ultima_training'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Authentication
AUTH_USER_MODEL = 'accounts.User'
SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Celery Configuration
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Payment Configuration
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID', default='')
PAYPAL_CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET', default='')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')

# Media and Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security Settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=False, cast=bool)

# ==============================================================================
# MODELS
# ==============================================================================

# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Business Admin'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    mobile = models.CharField(validators=[phone_regex], max_length=17)
    country_code = models.CharField(max_length=5, default='+98')
    organization = models.CharField(max_length=100, blank=True)
    
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_iranian(self):
        return self.country_code == '+98'

# courses/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

User = get_user_model()

class Course(models.Model):
    COURSE_TYPES = (
        ('online', 'Online'),
        ('in_person', 'In Person'),
        ('hybrid', 'Hybrid'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=160)
    detailed_description = models.TextField()
    
    instructor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='courses_taught',
        limit_choices_to={'user_type': 'instructor'}
    )
    co_instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses_co_taught',
        limit_choices_to={'user_type': 'instructor'}
    )
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    duration_hours = models.PositiveIntegerField()
    max_capacity = models.PositiveIntegerField(default=20)
    
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES, default='hybrid')
    prerequisites = models.TextField(blank=True)
    
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def enrolled_count(self):
        return self.enrollments.filter(status='enrolled').count()
    
    @property
    def available_spots(self):
        return self.max_capacity - self.enrolled_count

class CourseSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    online_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['start_datetime']
    
    def __str__(self):
        return f"{self.course.name} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, related_name='enrollments')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    tracking_number = models.CharField(max_length=20, unique=True)
    promo_code = models.CharField(max_length=50, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Approval fields
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_enrollments'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course', 'session']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.name}"
    
    def generate_tracking_number(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class Feedback(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='feedback')
    
    overall_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    overall_experience = models.TextField()
    instructor_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    venue_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    key_takeaways = models.TextField()
    improvements = models.TextField(blank=True)
    would_recommend = models.BooleanField()
    recommendation_comment = models.TextField(blank=True)
    
    allow_testimonial = models.BooleanField(default=False)
    
    # Review process
    is_approved = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_feedback'
    )
    review_date = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Feedback for {self.enrollment}"

# payments/models.py
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Enrollment
import uuid

User = get_user_model()

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer (Iran)'),
        ('stripe', 'Credit Card'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='payment')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    
    # Payment provider fields
    transaction_id = models.CharField(max_length=100, blank=True)
    rahgiri_code = models.CharField(max_length=50, blank=True)  # For Iranian payments
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    payment_metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount} {self.currency}"

class Refund(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='refund')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    
    # Iranian refund specific fields
    bank_card_number = models.CharField(max_length=20, blank=True)
    cardholder_name = models.CharField(max_length=100, blank=True)
    
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_refunds'
    )
    processed_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Refund {self.id} - {self.amount}"

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

# branding/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Testimonial(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='testimonials')
    
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField()
    
    student_name = models.CharField(max_length=100)  # For display purposes
    student_title = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Testimonial by {self.student_name}"

class MediaResource(models.Model):
    RESOURCE_TYPES = (
        ('video', 'Video'),
        ('pdf', 'PDF Document'),
        ('image', 'Image'),
        ('linkedin_post', 'LinkedIn Post'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    
    file = models.FileField(upload_to='media_resources/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    
    category = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=200, blank=True)
    
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Event(models.Model):
    EVENT_TYPES = (
        ('public_workshop', 'Public Workshop'),
        ('corporate_training', 'Corporate Training'),
        ('speaking_engagement', 'Speaking Engagement'),
        ('webinar', 'Webinar'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    online_link = models.URLField(blank=True)
    
    max_attendees = models.PositiveIntegerField(default=50)
    registration_deadline = models.DateTimeField()
    
    is_past_event = models.BooleanField(default=False)
    featured_image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_datetime']
    
    def __str__(self):
        return self.title

# ==============================================================================
# VIEWS
# ==============================================================================

# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User
from .forms import StudentRegistrationForm, UserProfileForm

class StudentRegistrationView(CreateView):
    model = User
    form_class = StudentRegistrationForm
    template_name = 'registration/student_register.html'
    success_url = reverse_lazy('account_login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 'student'
        user.save()
        messages.success(self.request, 'Registration successful! Please check your email to verify your account.')
        return super().form_valid(form)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

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
    ).select_related('course', 'session')
    
    # Pending feedback courses
    pending_feedback = Enrollment.objects.filter(
        student=user,
        status='completed',
        feedback__isnull=True
    ).select_related('course', 'session')
    
    # Completed courses with certificates
    completed_enrollments = Enrollment.objects.filter(
        student=user,
        status='completed',
        feedback__isnull=False,
        feedback__is_approved=True
    ).select_related('course', 'session', 'certificate')
    
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
        status='completed',
        feedback__isnull=False,
        feedback__is_approved=False
    ).select_related('student', 'course', 'feedback')
    
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
    
    # Admin statistics
    total_students = User.objects.filter(user_type='student').count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.filter(status='enrolled').count()
    pending_approvals = Enrollment.objects.filter(status='pending').count()
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'pending_approvals': pending_approvals,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
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

# payments/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from courses.models import Enrollment
from .models import Payment
from .forms import IranianPaymentForm

@login_required
def payment_process(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        student=request.user,
        status='pending'
    )
    
    # Check if payment already exists
    try:
        payment = enrollment.payment
        if payment.status == 'completed':
            messages.info(request, 'Payment already completed.')
            return redirect('student_dashboard')
    except Payment.DoesNotExist:
        # Create new payment record
        payment = Payment.objects.create(
            enrollment=enrollment,
            amount=enrollment.final_price,
            currency=enrollment.course.currency,
            payment_method='paypal' if not request.user.is_iranian else 'bank_transfer'
        )
    
    context = {
        'enrollment': enrollment,
        'payment': payment,
        'is_iranian': request.user.is_iranian,
    }
    
    if request.user.is_iranian:
        return render(request, 'payments/iranian_payment.html', context)
    else:
        return render(request, 'payments/international_payment.html', context)

@login_required
@csrf_exempt
def iranian_payment_complete(request, payment_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    payment = get_object_or_404(Payment, id=payment_id, enrollment__student=request.user)
    
    form = IranianPaymentForm(request.POST)
    if form.is_valid():
        rahgiri_code = form.cleaned_data['rahgiri_code']
        
        # Validate Rahgiri code (implement your validation logic)
        if validate_rahgiri_code(rahgiri_code, payment.amount):
            payment.rahgiri_code = rahgiri_code
            payment.status = 'completed'
            payment.payment_date = timezone.now()
            payment.save()
            
            # Update enrollment status
            payment.enrollment.status = 'enrolled'
            payment.enrollment.save()
            
            # Send confirmation email
            from .tasks import send_payment_confirmation_email
            send_payment_confirmation_email.delay(payment.id)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Payment completed successfully!',
                'redirect_url': '/dashboard/'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid Rahgiri code. Please check and try again.'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Please provide a valid Rahgiri code.'
    })

def validate_rahgiri_code(rahgiri_code, amount):
    """
    Implement your Rahgiri code validation logic here
    This should connect to the Iranian banking system API
    """
    # Placeholder implementation
    return len(rahgiri_code) >= 10

@csrf_exempt
def paypal_webhook(request):
    """Handle PayPal webhook notifications"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        event_type = data.get('event_type')
        
        if event_type == 'PAYMENT.CAPTURE.COMPLETED':
            # Extract payment information
            payment_id = data['resource']['id']
            amount = float(data['resource']['amount']['value'])
            
            # Find corresponding payment
            try:
                payment = Payment.objects.get(
                    transaction_id=payment_id,
                    payment_method='paypal'
                )
                payment.status = 'completed'
                payment.payment_date = timezone.now()
                payment.save()
                
                # Update enrollment
                payment.enrollment.status = 'enrolled'
                payment.enrollment.save()
                
                # Send confirmation email
                from .tasks import send_payment_confirmation_email
                send_payment_confirmation_email.delay(payment.id)
                
            except Payment.DoesNotExist:
                pass
        
        return JsonResponse({'status': 'success'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# certificates/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.conf import settings
import os

from .models import Certificate

@login_required
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(
        Certificate,
        id=certificate_id,
        enrollment__student=request.user,
        is_valid=True
    )
    
    if not certificate.certificate_file:
        raise Http404("Certificate file not found")
    
    file_path = certificate.certificate_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.certificate_number}.pdf"'
            return response
    
    raise Http404("Certificate file not found")

def verify_certificate(request, certificate_number):
    """Public certificate verification"""
    try:
        certificate = Certificate.objects.get(
            certificate_number=certificate_number,
            is_valid=True
        )
        context = {
            'certificate': certificate,
            'is_valid': True,
        }
    except Certificate.DoesNotExist:
        context = {
            'is_valid': False,
            'error': 'Certificate not found or invalid'
        }
    
    return render(request, 'certificates/verify.html', context)

# branding/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Testimonial, MediaResource, Event
from .forms import ContactForm, SpeakingRequestForm

def homepage(request):
    """Dr. Josef Balahan homepage"""
    featured_testimonials = Testimonial.objects.filter(
        is_featured=True,
        is_approved=True
    )[:6]
    
    upcoming_events = Event.objects.filter(
        start_datetime__gte=timezone.now(),
        is_past_event=False
    )[:3]
    
    context = {
        'testimonials': featured_testimonials,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'branding/homepage.html', context)

def about_view(request):
    """About Dr. Josef Balahan"""
    return render(request, 'branding/about.html')

def workshops_events(request):
    """Workshops and events listing"""
    events = Event.objects.all().order_by('-start_datetime')
    
    # Filter by type
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)
    
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    context = {'events': events}
    return render(request, 'branding/workshops_events.html', context)

def testimonials_view(request):
    """Testimonials page"""
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    
    paginator = Paginator(testimonials, 12)
    page_number = request.GET.get('page')
    testimonials = paginator.get_page(page_number)
    
    context = {'testimonials': testimonials}
    return render(request, 'branding/testimonials.html', context)

def media_resources(request):
    """Media and resources page"""
    resources = MediaResource.objects.filter(is_public=True).order_by('-created_at')
    
    # Filter by type
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        resources = resources.filter(category=category)
    
    context = {'resources': resources}
    return render(request, 'branding/media_resources.html', context)

def contact_view(request):
    """Contact and booking form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email notification
            from .tasks import send_contact_notification
            send_contact_notification.delay(form.cleaned_data)
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'branding/contact.html', context)

def speaking_request(request):
    """Speaking engagement request form"""
    if request.method == 'POST':
        form = SpeakingRequestForm(request.POST)
        if form.is_valid():
            # Send email notification
            from .tasks import send_speaking_request_notification
            send_speaking_request_notification.delay(form.cleaned_data)
            
            messages.success(request, 'Your speaking request has been submitted successfully!')
            return redirect('homepage')
    else:
        form = SpeakingRequestForm()
    
    context = {'form': form}
    return render(request, 'branding/speaking_request.html', context)

# ==============================================================================
# FORMS
# ==============================================================================

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'middle_name', 'last_name', 
                 'mobile', 'country_code', 'organization', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'country_code': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country_code'].choices = [
            ('+1', 'United States (+1)'),
            ('+44', 'United Kingdom (+44)'),
            ('+49', 'Germany (+49)'),
            ('+33', 'France (+33)'),
            ('+98', 'Iran (+98)'),
            ('+971', 'UAE (+971)'),
            ('+966', 'Saudi Arabia (+966)'),
        ]
        self.fields['middle_name'].required = False
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'mobile', 
                 'country_code', 'organization', 'profile_picture', 'bio')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'country_code': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# courses/forms.py
from django import forms
from .models import Enrollment, Feedback, CourseSession

class CourseRegistrationForm(forms.ModelForm):
    session = forms.ModelChoiceField(
        queryset=CourseSession.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select date and location"
    )
    promo_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter promo code (optional)'})
    )
    
    class Meta:
        model = Enrollment
        fields = ['session', 'promo_code']
    
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        
        if course:
            self.fields['session'].queryset = course.sessions.filter(
                start_datetime__gte=timezone.now(),
                is_active=True
            ).order_by('start_datetime')
    
    def save(self, commit=True):
        enrollment = super().save(commit=False)
        enrollment.final_price = enrollment.session.course.price
        
        # Apply promo code if valid
        promo_code = self.cleaned_data.get('promo_code')
        if promo_code:
            # Implement promo code logic here
            pass
        
        if commit:
            enrollment.save()
        return enrollment

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'overall_rating', 'overall_experience', 'instructor_rating',
            'content_rating', 'venue_rating', 'key_takeaways', 'improvements',
            'would_recommend', 'recommendation_comment', 'allow_testimonial'
        ]
        widgets = {
            'overall_rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'overall_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 500}),
            'instructor_rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'content_rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'venue_rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'key_takeaways': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'improvements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'would_recommend': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}),
            'recommendation_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'allow_testimonial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# payments/forms.py
from django import forms
from .models import Refund

class IranianPaymentForm(forms.Form):
    rahgiri_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Rahgiri Code',
            'required': True
        })
    )

class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['amount', 'reason', 'bank_card_number', 'cardholder_name']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bank_card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last 4 digits only'}),
            'cardholder_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        payment = kwargs.pop('payment', None)
        super().__init__(*args, **kwargs)
        
        if payment:
            self.fields['amount'].initial = payment.amount
            
            # Show Iranian-specific fields only for Iranian payments
            if payment.payment_method != 'bank_transfer':
                del self.fields['bank_card_number']
                del self.fields['cardholder_name']

# branding/forms.py
from django import forms

class ContactForm(forms.Form):
    PURPOSE_CHOICES = [
        ('speaking', 'Speaking Request'),
        ('corporate', 'Corporate Training'),
        ('general', 'General Inquiry'),
    ]
    
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    company = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    purpose = forms.ChoiceField(choices=PURPOSE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

class SpeakingRequestForm(forms.Form):
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('corporate', 'Corporate Event'),
        ('webinar', 'Webinar'),
    ]
    
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    company = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    event_type = forms.ChoiceField(choices=EVENT_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))
    event_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    audience_size = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    budget_range = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    topics = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    additional_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

# ==============================================================================
# TASKS (Celery)
# ==============================================================================

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

# branding/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

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
        print(f"Error sending contact notification: {e}")

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
        print(f"Error sending speaking request notification: {e}")

# ==============================================================================
# URLS
# ==============================================================================

# ultima_training/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('courses/', include('courses.urls')),
    path('payments/', include('payments.urls')),
    path('certificates/', include('certificates.urls')),
    path('', include('branding.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name='student_register'),
    path('profile/', views.profile_view, name='profile'),
]

# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]

# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<uuid:course_id>/', views.course_detail, name='course_detail'),
    path('<uuid:course_id>/register/', views.course_register, name='course_register'),
    path('enrollment/<uuid:enrollment_id>/cancel/', views.cancel_enrollment, name='cancel_enrollment'),
    path('enrollment/<uuid:enrollment_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    
    # Instructor URLs
    path('instructor/approve/<uuid:enrollment_id>/', views.instructor_approve_student, name='instructor_approve_student'),
    path('instructor/feedback/<int:feedback_id>/review/', views.instructor_review_feedback, name='instructor_review_feedback'),
]

# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('process/<uuid:enrollment_id>/', views.payment_process, name='payment_process'),
    path('iranian/<uuid:payment_id>/complete/', views.iranian_payment_complete, name='iranian_payment_complete'),
    path('webhooks/paypal/', views.paypal_webhook, name='paypal_webhook'),
]

# certificates/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('download/<uuid:certificate_id>/', views.download_certificate, name='download_certificate'),
    path('verify/<str:certificate_number>/', views.verify_certificate, name='verify_certificate'),
]

# branding/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about_view, name='about'),
    path('workshops-events/', views.workshops_events, name='workshops_events'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('media-resources/', views.media_resources, name='media_resources'),
    path('contact/', views.contact_view, name='contact'),
    path('speaking-request/', views.speaking_request, name='speaking_request'),
]

# ==============================================================================
# TEMPLATES
# ==============================================================================

# templates/base.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Ultima Training - Dr. Josef Balahan{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="{% load static %}{% static 'css/style.css' %}" rel="stylesheet">
    
    {% block extra_css %}{% endblock %}
</head>
<body class="bg-dark text-light">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="{% url 'homepage' %}">
                <img src="{% static 'images/logo.png' %}" alt="Ultima Training" height="40" class="me-2">
                ULTIMA TRAINING
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'homepage' %}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'about' %}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'course_list' %}">Courses</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'workshops_events' %}">Events</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'testimonials' %}">Testimonials</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'media_resources' %}">Resources</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'contact' %}">Contact</a>
                    </li>
                </ul>
                
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-user-circle me-1"></i>
                                {{ user.get_full_name }}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark">
                                {% if user.user_type == 'student' %}
                                    <li><a class="dropdown-item" href="{% url 'student_dashboard' %}">Dashboard</a></li>
                                {% elif user.user_type == 'instructor' %}
                                    <li><a class="dropdown-item" href="{% url 'instructor_dashboard' %}">Dashboard</a></li>
                                {% elif user.user_type == 'admin' %}
                                    <li><a class="dropdown-item" href="{% url 'admin_dashboard' %}">Dashboard</a></li>
                                {% endif %}
                                <li><a class="dropdown-item" href="{% url 'profile' %}">Profile</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{% url 'account_logout' %}">Logout</a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'account_login' %}">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'student_register' %}">Register</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="pt-5 mt-4">
        {% if messages %}
            <div class="container mt-3">
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-black text-light py-5 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h5>Contact Information</h5>
                    <p>
                        <i class="fas fa-envelope me-2"></i>
                        info@ultimatraining.com
                    </p>
                    <p>
                        <i class="fas fa-phone me-2"></i>
                        +98 21 1234 5678
                    </p>
                </div>
                <div class="col-md-4">
                    <h5>Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="{% url 'course_list' %}" class="text-light text-decoration-none">Courses</a></li>
                        <li><a href="{% url 'workshops_events' %}" class="text-light text-decoration-none">Events</a></li>
                        <li><a href="{% url 'about' %}" class="text-light text-decoration-none">About Dr. Balahan</a></li>
                        <li><a href="{% url 'contact' %}" class="text-light text-decoration-none">Contact Us</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>Follow Dr. Josef Balahan</h5>
                    <div>
                        <a href="#" class="text-light me-3"><i class="fab fa-linkedin fa-2x"></i></a>
                        <a href="#" class="text-light me-3"><i class="fab fa-twitter fa-2x"></i></a>
                        <a href="#" class="text-light me-3"><i class="fab fa-youtube fa-2x"></i></a>
                    </div>
                </div>
            </div>
            <hr class="my-4">
            <div class="text-center">
                <p>&copy; 2024 Ultima Training. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
"""

# templates/dashboard/student_dashboard.html
"""
{% extends 'base.html' %}
{% load static %}

{% block title %}Student Dashboard - Ultima Training{% endblock %}

{% block content %}
<div class="container py-4">
    <div class="row">
        <div class="col-12">
            <h1 class="mb-4">
                <i class="fas fa-tachometer-alt me-2"></i>
                Welcome back, {{ user.get_full_name }}
            </h1>
        </div>
    </div>

    <!-- Registered Courses -->
    <div class="row mb-5">
        <div class="col-12">
            <div class="card bg-dark border-secondary">
                <div class="card-header bg-purple">
                    <h3 class="card-title mb-0">
                        <i class="fas fa-calendar-check me-2"></i>
                        Upcoming Courses
                    </h3>
                </div>
                <div class="card-body">
                    {% if registered_enrollments %}
                        <div class="row">
                            {% for enrollment in registered_enrollments %}
                                <div class="col-md-6 col-lg-4 mb-3">
                                    <div class="card bg-secondary">
                                        <div class="card-body">
                                            <h5 class="card-title">{{ enrollment.course.name }}</h5>
                                            <p class="card-text">
                                                <i class="fas fa-calendar me-2"></i>
                                                {{ enrollment.session.start_datetime|date:"M d, Y" }}
                                            </p>
                                            <p class="card-text">
                                                <i class="fas fa-map-marker-alt me-2"></i>
                                                {{ enrollment.session.location }}
                                            </p>
                                            <span class="badge bg-{{ enrollment.status|yesno:'success,warning' }} mb-2">
                                                {{ enrollment.get_status_display }}
                                            </span>
                                            <div class="d-grid gap-2">
                                                <button class="btn btn-outline-light btn-sm" 
                                                        onclick="showCourseDetails('{{ enrollment.id }}')">
                                                    View Details
                                                </button>
                                                {% if enrollment.session.start_datetime > now %}
                                                    <a href="{% url 'cancel_enrollment' enrollment.id %}" 
                                                       class="btn btn-outline-danger btn-sm">
                                                        Cancel Registration
                                                    </a>
                                                {% endif %}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-4">
                            <i class="fas fa-graduation-cap fa-3x text-muted mb-3"></i>
                            <h4 class="text-muted">No upcoming courses</h4>
                            <p class="text-muted">Browse our courses and register for your next learning adventure!</p>
                            <a href="{% url 'course_list' %}" class="btn btn-purple">Browse Courses</a>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- Pending Feedback -->
    <div class="row mb-5">
        <div class="col-12">
            <div class="card bg-dark border-secondary">
                <div class="card-header bg-warning text-dark">
                    <h3 class="card-title mb-0">
                        <i class="fas fa-comment-alt me-2"></i>
                        Awaiting Your Feedback
                    </h3>
                </div>
                <div class="card-body">
                    {% if pending_feedback %}
                        <div class="row">
                            {% for enrollment in pending_feedback %}
                                <div class="col-md-6 col-lg-4 mb-3">
                                    <div class="card bg-secondary">
                                        <div class="card-body">
                                            <h5 class="card-title">{{ enrollment.course.name }}</h5>
                                            <p class="card-text">
                                                <i class="fas fa-calendar-check me-2"></i>
                                                Completed: {{ enrollment.completion_date|date:"M d, Y" }}
                                            </p>
                                            <div class="d-grid">
                                                <a href="{% url 'submit_feedback' enrollment.id %}" 
                                                   class="btn btn-warning text-dark">
                                                    Submit Feedback
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-3">
                            <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
                            <p class="text-muted">All feedback submitted!</p>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- Completed Courses -->
    <div class="row">
        <div class="col-12">
            <div class="card bg-dark border-secondary">
                <div class="card-header bg-success">
                    <h3 class="card-title mb-0">
                        <i class="fas fa-medal me-2"></i>
                        Completed Courses
                    </h3>
                </div>
                <div class="card-body">
                    {% if completed_enrollments %}
                        <div class="row">
                            {% for enrollment in completed_enrollments %}
                                <div class="col-md-6 col-lg-4 mb-3">
                                    <div class="card bg-secondary">
                                        <div class="card-body">
                                            <h5 class="card-title">{{ enrollment.course.name }}</h5>
                                            <p class="card-text">
                                                <i class="fas fa-calendar-check me-2"></i>
                                                Completed: {{ enrollment.completion_date|date:"M d, Y" }}
                                            </p>
                                            <div class="d-grid gap-2">
                                                {% if enrollment.certificate %}
                                                    <a href="{% url 'download_certificate' enrollment.certificate.id %}" 
                                                       class="btn btn-success btn-sm">
                                                        <i class="fas fa-download me-1"></i>
                                                        Download Certificate
                                                    </a>
                                                {% endif %}
                                                <button class="btn btn-outline-light btn-sm">
                                                    <i class="fas fa-award me-1"></i>
                                                    Download Badge
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-3">
                            <i class="fas fa-hourglass-half fa-2x text-muted mb-2"></i>
                            <p class="text-muted">No completed courses yet. Keep learning!</p>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Course Details Modal -->
<div class="modal fade" id="courseDetailsModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h5 class="modal-title">Course Details</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="courseDetailsContent">
                <!-- Content loaded via AJAX -->
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
function showCourseDetails(enrollmentId) {
    $('#courseDetailsModal').modal('show');
    // Load course details via AJAX
    // Implementation details...
}
</script>
{% endblock %}
"""

# templates/payments/iranian_payment.html
"""
{% extends 'base.html' %}
{% load static %}

{% block title %}Payment - Ultima Training{% endblock %}

{% block content %}
<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card bg-dark border-secondary">
                <div class="card-header bg-purple">
                    <h3 class="card-title mb-0">
                        <i class="fas fa-credit-card me-2"></i>
                        Complete Your Payment
                    </h3>
                </div>
                <div class="card-body">
                    <!-- Order Summary -->
                    <div class="row mb-4">
                        <div class="col-12">
                            <h5>Order Summary</h5>
                            <div class="card bg-secondary">
                                <div class="card-body">
                                    <h6>{{ enrollment.course.name }}</h6>
                                    <p class="mb-1">
                                        <i class="fas fa-calendar me-2"></i>
                                        {{ enrollment.session.start_datetime|date:"M d, Y H:i" }}
                                    </p>
                                    <p class="mb-1">
                                        <i class="fas fa-map-marker-alt me-2"></i>
                                        {{ enrollment.session.location }}
                                    </p>
                                    <hr>
                                    <div class="d-flex justify-content-between">
                                        <strong>Total Amount:</strong>
                                        <strong>{{ payment.amount }} IRR</strong>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Payment Instructions -->
                    <div class="alert alert-info">
                        <h5 class="alert-heading">
                            <i class="fas fa-info-circle me-2"></i>
                            Payment Instructions
                        </h5>
                        <p>Please transfer the amount using your mobile banking to the following account:</p>
                        <div class="text-center p-3 bg-light text-dark rounded">
                            <h4><strong>xxxx-xxxx-xxxx-xxxx</strong></h4>
                            <p class="mb-0">Account Holder: Ultima Training</p>
                        </div>
                        <p class="mt-3 mb-0">After completing the payment, enter your Rahgiri Code below to confirm your registration.</p>
                    </div>

                    <!-- Payment Form -->
                    <form id="iranianPaymentForm">
                        {% csrf_token %}
                        <div class="mb-3">
                            <label for="rahgiriCode" class="form-label">
                                Rahgiri Code <span class="text-danger">*</span>
                            </label>
                            <input type="text" class="form-control" id="rahgiriCode" name="rahgiri_code" 
                                   placeholder="Enter your Rahgiri Code" required>
                            <div class="form-text">This code is provided by your bank after successful payment.</div>
                        </div>

                        <!-- Session Timer -->
                        <div class="alert alert-warning">
                            <i class="fas fa-clock me-2"></i>
                            Session expires in: <strong id="sessionTimer">5:00</strong> minutes
                        </div>

                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-success btn-lg" id="completePaymentBtn">
                                <i class="fas fa-check me-2"></i>
                                Complete Registration
                            </button>
                            <a href="{% url 'student_dashboard' %}" class="btn btn-outline-secondary">
                                Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
// Session timer
let timeLeft = 300; // 5 minutes in seconds
const timerElement = document.getElementById('sessionTimer');

function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    
    if (timeLeft <= 0) {
        alert('Session expired. Please start the payment process again.');
        window.location.href = '{% url "student_dashboard" %}';
        return;
    }
    
    timeLeft--;
}

setInterval(updateTimer, 1000);

// Payment form submission
document.getElementById('iranianPaymentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const rahgiriCode = document.getElementById('rahgiriCode').value;
    const submitBtn = document.getElementById('completePaymentBtn');
    
    if (!rahgiriCode.trim()) {
        alert('Please enter your Rahgiri Code');
        return;
    }
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    
    fetch('{% url "iranian_payment_complete" payment.id %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `rahgiri_code=${encodeURIComponent(rahgiriCode)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            window.location.href = data.redirect_url;
        } else {
            alert(data.message);
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Complete Registration';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Complete Registration';
    });
});
</script>
{% endblock %}
"""

# templates/courses/submit_feedback.html
"""
{% extends 'base.html' %}
{% load static %}

{% block title %}Submit Feedback - {{ enrollment.course.name }}{% endblock %}

{% block content %}
<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-md-10">
            <div class="card bg-dark border-secondary">
                <div class="card-header bg-purple">
                    <h3 class="card-title mb-0">
                        <i class="fas fa-comment-alt me-2"></i>
                        Course Feedback
                    </h3>
                    <p class="mb-0 mt-2">{{ enrollment.course.name }}</p>
                </div>
                <div class="card-body">
                    <form method="post" id="feedbackForm">
                        {% csrf_token %}
                        
                        <!-- Overall Rating -->
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <label class="form-label">Overall Course Rating</label>
                                <div class="star-rating" data-rating="overall_rating">
                                    <i class="fas fa-star" data-value="1"></i>
                                    <i class="fas fa-star" data-value="2"></i>
                                    <i class="fas fa-star" data-value="3"></i>
                                    <i class="fas fa-star" data-value="4"></i>
                                    <i class="fas fa-star" data-value="5"></i>
                                </div>
                                <input type="hidden" name="overall_rating" id="overall_rating">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Instructor Effectiveness</label>
                                <div class="star-rating" data-rating="instructor_rating">
                                    <i class="fas fa-star" data-value="1"></i>
                                    <i class="fas fa-star" data-value="2"></i>
                                    <i class="fas fa-star" data-value="3"></i>
                                    <i class="fas fa-star" data-value="4"></i>
                                    <i class="fas fa-star" data-value="5"></i>
                                </div>
                                <input type="hidden" name="instructor_rating" id="instructor_rating">
                            </div>
                        </div>
                        
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <label class="form-label">Course Content Quality</label>
                                <div class="star-rating" data-rating="content_rating">
                                    <i class="fas fa-star" data-value="1"></i>
                                    <i class="fas fa-star" data-value="2"></i>
                                    <i class="fas fa-star" data-value="3"></i>
                                    <i class="fas fa-star" data-value="4"></i>
                                    <i class="fas fa-star" data-value="5"></i>
                                </div>
                                <input type="hidden" name="content_rating" id="content_rating">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Venue/Platform Rating</label>
                                <div class="star-rating" data-rating="venue_rating">
                                    <i class="fas fa-star" data-value="1"></i>
                                    <i class="fas fa-star" data-value="2"></i>
                                    <i class="fas fa-star" data-value="3"></i>
                                    <i class="fas fa-star" data-value="4"></i>
                                    <i class="fas fa-star" data-value="5"></i>
                                </div>
                                <input type="hidden" name="venue_rating" id="venue_rating">
                            </div>
                        </div>

                        <!-- Text Feedback -->
                        <div class="mb-3">
                            <label for="overall_experience" class="form-label">Overall Experience</label>
                            <textarea class="form-control" id="overall_experience" name="overall_experience" 
                                      rows="4" maxlength="500" 
                                      placeholder="Please describe your overall experience with this course..."></textarea>
                            <div class="form-text">Maximum 500 characters</div>
                        </div>

                        <div class="mb-3">
                            <label for="key_takeaways" class="form-label">Key Takeaways</label>
                            <textarea class="form-control" id="key_takeaways" name="key_takeaways" 
                                      rows="3" 
                                      placeholder="What were the most valuable things you learned?"></textarea>
                        </div>

                        <div class="mb-3">
                            <label for="improvements" class="form-label">Suggestions for Improvement</label>
                            <textarea class="form-control" id="improvements" name="improvements" 
                                      rows="3" 
                                      placeholder="What could be improved in future sessions?"></textarea>
                        </div>

                        <!-- Recommendation -->
                        <div class="mb-3">
                            <label class="form-label">Would you recommend this course?</label>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="would_recommend" 
                                       id="recommend_yes" value="True">
                                <label class="form-check-label" for="recommend_yes">Yes</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="would_recommend" 
                                       id="recommend_no" value="False">
                                <label class="form-check-label" for="recommend_no">No</label>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="recommendation_comment" class="form-label">Recommendation Comment</label>
                            <textarea class="form-control" id="recommendation_comment" name="recommendation_comment" 
                                      rows="2" 
                                      placeholder="Please explain your recommendation..."></textarea>
                        </div>

                        <!-- Testimonial Permission -->
                        <div class="mb-4">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="allow_testimonial" 
                                       id="allow_testimonial">
                                <label class="form-check-label" for="allow_testimonial">
                                    I give permission to use my feedback as a testimonial on the website
                                </label>
                            </div>
                        </div>

                        <!-- Form Actions -->
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <button type="button" class="btn btn-outline-secondary" onclick="saveDraft()">
                                <i class="fas fa-save me-2"></i>Save Draft
                            </button>
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-paper-plane me-2"></i>Submit for Review
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_css %}
<style>
.star-rating {
    display: flex;
    gap: 5px;
    margin-bottom: 10px;
}

.star-rating i {
    font-size: 24px;
    color: #6c757d;
    cursor: pointer;
    transition: color 0.2s;
}

.star-rating i:hover,
.star-rating i.active {
    color: #ffc107;
}
</style>
{% endblock %}

{% block extra_js %}
<script>
// Star rating functionality
document.querySelectorAll('.star-rating').forEach(rating => {
    const stars = rating.querySelectorAll('i');
    const fieldName = rating.dataset.rating;
    const hiddenInput = document.getElementById(fieldName);
    
    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            const value = index + 1;
            hiddenInput.value = value;
            
            // Update visual state
            stars.forEach((s, i) => {
                if (i < value) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
        });
        
        star.addEventListener('mouseover', () => {
            stars.forEach((s, i) => {
                if (i <= index) {
                    s.style.color = '#ffc107';
                } else {
                    s.style.color = '#6c757d';
                }
            });
        });
    });
    
    rating.addEventListener('mouseleave', () => {
        const currentValue = parseInt(hiddenInput.value) || 0;
        stars.forEach((s, i) => {
            if (i < currentValue) {
                s.style.color = '#ffc107';
            } else {
                s.style.color = '#6c757d';
            }
        });
    });
});

// Character counter
document.getElementById('overall_experience').addEventListener('input', function() {
    const maxLength = 500;
    const currentLength = this.value.length;
    const remaining = maxLength - currentLength;
    
    let helpText = this.parentElement.querySelector('.form-text');
    helpText.textContent = `${remaining} characters remaining`;
    
    if (remaining < 50) {
        helpText.classList.add('text-warning');
    } else {
        helpText.classList.remove('text-warning');
    }
});

// Save draft functionality
function saveDraft() {
    const formData = new FormData(document.getElementById('feedbackForm'));
    
    // Save to sessionStorage
    const draftData = {};
    for (let [key, value] of formData.entries()) {
        draftData[key] = value;
    }
    
    sessionStorage.setItem('feedback_draft_{{ enrollment.id }}', JSON.stringify(draftData));
    
    // Show confirmation
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        Draft saved successfully!
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.row'));
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Load draft on page load
window.addEventListener('load', function() {
    const draftData = sessionStorage.getItem('feedback_draft_{{ enrollment.id }}');
    if (draftData) {
        const data = JSON.parse(draftData);
        
        Object.keys(data).forEach(key => {
            const field = document.querySelector(`[name="${key}"]`);
            if (field) {
                if (field.type === 'radio') {
                    const radio = document.querySelector(`[name="${key}"][value="${data[key]}"]`);
                    if (radio) radio.checked = true;
                } else if (field.type === 'checkbox') {
                    field.checked = data[key] === 'on';
                } else {
                    field.value = data[key];
                    
                    // Update star ratings
                    if (key.includes('rating')) {
                        const rating = document.querySelector(`[data-rating="${key}"]`);
                        if (rating) {
                            const stars = rating.querySelectorAll('i');
                            const value = parseInt(data[key]);
                            stars.forEach((s, i) => {
                                if (i < value) {
                                    s.classList.add('active');
                                }
                            });
                        }
                    }
                }
            }
        });
    }
});

// Form validation
document.getElementById('feedbackForm').addEventListener('submit', function(e) {
    const requiredRatings = ['overall_rating', 'instructor_rating', 'content_rating', 'venue_rating'];
    let isValid = true;
    
    requiredRatings.forEach(rating => {
        const value = document.getElementById(rating).value;
        if (!value || value === '0') {
            isValid = false;
            const ratingDiv = document.querySelector(`[data-rating="${rating}"]`);
            ratingDiv.style.border = '2px solid #dc3545';
            ratingDiv.style.borderRadius = '5px';
            ratingDiv.style.padding = '5px';
        }
    });
    
    if (!isValid) {
        e.preventDefault();
        alert('Please provide ratings for all categories before submitting.');
        return;
    }
    
    // Clear draft after successful submission
    sessionStorage.removeItem('feedback_draft_{{ enrollment.id }}');
});
</script>
{% endblock %}
"""

# templates/branding/homepage.html
"""
{% extends 'base.html' %}
{% load static %}

{% block title %}Dr. Josef Balahan - 40+ Years of Agile Excellence{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero-section bg-gradient-purple text-white py-5">
    <div class="container">
        <div class="row align-items-center min-vh-75">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold mb-4 animate-fade-in">
                    40+ Years of Agile Excellence
                </h1>
                <p class="lead mb-4 animate-fade-in-delay-1">
                    Transforming organizations worldwide through proven Agile and Scrum methodologies. 
                    Join thousands of professionals who have accelerated their careers with Dr. Josef Balahan.
                </p>
                <div class="d-grid gap-2 d-md-flex animate-fade-in-delay-2">
                    <a href="{% url 'course_list' %}" class="btn btn-light btn-lg px-4 me-md-2">
                        <i class="fas fa-graduation-cap me-2"></i>Book Workshop
                    </a>
                    <a href="{% url 'speaking_request' %}" class="btn btn-outline-light btn-lg px-4">
                        <i class="fas fa-microphone me-2"></i>Request Speaking
                    </a>
                    <a href="#" class="btn btn-outline-light btn-lg px-4" onclick="downloadBrochure()">
                        <i class="fas fa-download me-2"></i>Download Brochure
                    </a>
                </div>
            </div>
            <div class="col-lg-6 text-center animate-fade-in-delay-3">
                <img src="{% static 'images/dr-josef-balahan.jpg' %}" 
                     alt="Dr. Josef Balahan" 
                     class="img-fluid rounded-circle shadow-lg hero-image">
            </div>
        </div>
    </div>
</section>

<!-- About Section -->
<section class="py-5 bg-dark">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 mx-auto text-center">
                <h2 class="display-5 fw-bold mb-4">Meet Dr. Josef Balahan</h2>
                <p class="lead text-muted mb-4">
                    A pioneering figure in Agile transformation with over four decades of experience 
                    in software development, project management, and organizational change.
                </p>
                <div class="row text-center mb-4">
                    <div class="col-md-3 col-6 mb-3">
                        <div class="stat-card">
                            <h3 class="text-purple fw-bold">40+</h3>
                            <p class="text-muted">Years Experience</p>
                        </div>
                    </div>
                    <div class="col-md-3 col-6 mb-3">
                        <div class="stat-card">
                            <h3 class="text-purple fw-bold">500+</h3>
                            <p class="text-muted">Companies Transformed</p>
                        </div>
                    </div>
                    <div class="col-md-3 col-6 mb-3">
                        <div class="stat-card">
                            <h3 class="text-purple fw-bold">10,000+</h3>
                            <p class="text-muted">Professionals Trained</p>
                        </div>
                    </div>
                    <div class="col-md-3 col-6 mb-3">
                        <div class="stat-card">
                            <h3 class="text-purple fw-bold">50+</h3>
                            <p class="text-muted">Countries Reached</p>
                        </div>
                    </div>
                </div>
                <a href="{% url 'about' %}" class="btn btn-purple btn-lg">
                    Learn More About Dr. Balahan
                </a>
            </div>
        </div>
    </div>
</section>

<!-- Upcoming Events -->
<section class="py-5 bg-secondary">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h2 class="text-center mb-5">Upcoming Events</h2>
                {% if upcoming_events %}
                    <div class="row">
                        {% for event in upcoming_events %}
                            <div class="col-md-4 mb-4">
                                <div class="card bg-dark border-secondary h-100">
                                    {% if event.featured_image %}
                                        <img src="{{ event.featured_image.url }}" class="card-img-top" alt="{{ event.title }}">
                                    {% endif %}
                                    <div class="card-body d-flex flex-column">
                                        <span class="badge bg-purple mb-2 align-self-start">{{ event.get_event_type_display }}</span>
                                        <h5 class="card-title">{{ event.title }}</h5>
                                        <p class="card-text flex-grow-1">{{ event.description|truncatewords:20 }}</p>
                                        <div class="mt-auto">
                                            <p class="text-muted mb-2">
                                                <i class="fas fa-calendar me-2"></i>
                                                {{ event.start_datetime|date:"M d, Y" }}
                                            </p>
                                            <p class="text-muted mb-3">
                                                <i class="fas fa-map-marker-alt me-2"></i>
                                                {{ event.location|default:"Online" }}
                                            </p>
                                            <a href="#" class="btn btn-purple">Register Now</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="text-center">
                        <i class="fas fa-calendar-alt fa-3x text-muted mb-3"></i>
                        <h4 class="text-muted">No upcoming events</h4>
                        <p class="text-muted">Check back soon for new workshops and speaking engagements!</p>
                    </div>
                {% endif %}
                <div class="text-center mt-4">
                    <a href="{% url 'workshops_events' %}" class="btn btn-outline-light">
                        View All Events
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Testimonials -->
<section class="py-5 bg-dark">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h2 class="text-center mb-5">What Our Students Say</h2>
                {% if testimonials %}
                    <div id="testimonialCarousel" class="carousel slide" data-bs-ride="carousel">
                        <div class="carousel-inner">
                            {% for testimonial in testimonials %}
                                <div class="carousel-item {% if forloop.first %}active{% endif %}">
                                    <div class="row justify-content-center">
                                        <div class="col-lg-8">
                                            <div class="card bg-secondary border-0 text-center">
                                                <div class="card-body p-5">
                                                    <div class="mb-3">
                                                        {% for i in "12345" %}
                                                            {% if forloop.counter <= testimonial.rating %}
                                                                <i class="fas fa-star text-warning"></i>
                                                            {% else %}
                                                                <i class="far fa-star text-warning"></i>
                                                            {% endif %}
                                                        {% endfor %}
                                                    </div>
                                                    <blockquote class="blockquote mb-4">
                                                        <p class="lead">"{{ testimonial.content }}"</p>
                                                    </blockquote>
                                                    <div class="d-flex align-items-center justify-content-center">
                                                        {% if testimonial.student.profile_picture %}
                                                            <img src="{{ testimonial.student.profile_picture.url }}" 
                                                                 alt="{{ testimonial.student_name }}" 
                                                                 class="rounded-circle me-3" width="60" height="60">
                                                        {% endif %}
                                                        <div class="text-start">
                                                            <h6 class="mb-0">{{ testimonial.student_name }}</h6>
                                                            <small class="text-muted">{{ testimonial.student_title }}</small>
                                                            {% if testimonial.company_name %}
                                                                <br><small class="text-muted">{{ testimonial.company_name }}</small>
                                                            {% endif %}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#testimonialCarousel" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon"></span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#testimonialCarousel" data-bs-slide="next">
                            <span class="carousel-control-next-icon"></span>
                        </button>
                    </div>
                {% endif %}
                <div class="text-center mt-4">
                    <a href="{% url 'testimonials' %}" class="btn btn-outline-light">
                        Read More Testimonials
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Call to Action -->
<section class="py-5 bg-gradient-purple text-white">
    <div class="container">
        <div class="row text-center">
            <div class="col-lg-8 mx-auto">
                <h2 class="display-5 fw-bold mb-4">Ready to Transform Your Career?</h2>
                <p class="lead mb-4">
                    Join thousands of professionals who have accelerated their careers through our comprehensive Agile and Scrum training programs.
                </p>
                <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                    <a href="{% url 'course_list' %}" class="btn btn-light btn-lg px-4 me-md-2">
                        Browse Courses
                    </a>
                    <a href="{% url 'contact' %}" class="btn btn-outline-light btn-lg px-4">
                        Contact Us
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

{% block extra_css %}
<style>
.bg-gradient-purple {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.text-purple {
    color: #667eea !important;
}

.btn-purple {
    background-color: #667eea;
    border-color: #667eea;
    color: white;
}

.btn-purple:hover {
    background-color: #5a6fd8;
    border-color: #5a6fd8;
}

.hero-image {
    max-width: 400px;
    transition: transform 0.3s ease;
}

.hero-image:hover {
    transform: scale(1.05);
}

.min-vh-75 {
    min-height: 75vh;
}

.animate-fade-in {
    animation: fadeInUp 1s ease-out;
}

.animate-fade-in-delay-1 {
    animation: fadeInUp 1s ease-out 0.2s both;
}

.animate-fade-in-delay-2 {
    animation: fadeInUp 1s ease-out 0.4s both;
}

.animate-fade-in-delay-3 {
    animation: fadeInUp 1s ease-out 0.6s both;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stat-card {
    padding: 20px;
    border-radius: 10px;
    background: rgba(102, 126, 234, 0.1);
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
}
</style>
{% endblock %}

{% block extra_js %}
<script>
function downloadBrochure() {
    // Implement brochure download
    const link = document.createElement('a');
    link.href = '{% static "downloads/ultima-training-brochure.pdf" %}';
    link.download = 'Ultima-Training-Brochure.pdf';
    link.click();
}

// Auto-play testimonial carousel
const testimonialCarousel = document.getElementById('testimonialCarousel');
if (testimonialCarousel) {
    new bootstrap.Carousel(testimonialCarousel, {
        interval: 5000,
        wrap: true
    });
}
</script>
{% endblock %}
"""

# static/css/style.css
"""
/* Custom CSS for Ultima Training Platform */

:root {
    --primary-purple: #667eea;
    --secondary-purple: #764ba2;
    --dark-bg: #1a1a1a;
    --card-bg: #2d2d2d;
    --border-color: #404040;
}

body {
    background-color: var(--dark-bg);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Custom button styles */
.btn-purple {
    background-color: var(--primary-purple);
    border-color: var(--primary-purple);
    color: white;
    transition: all 0.3s ease;
}

.btn-purple:hover {
    background-color: var(--secondary-purple);
    border-color: var(--secondary-purple);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Navigation */
.navbar-brand {
    font-weight: 700;
    letter-spacing: 1px;
}

.nav-link {
    transition: color 0.3s ease;
    position: relative;
}

.nav-link:hover {
    color: var(--primary-purple) !important;
}

.nav-link::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: 0;
    left: 50%;
    background-color: var(--primary-purple);
    transition: all 0.3s ease;
}

.nav-link:hover::after {
    width: 100%;
    left: 0;
}

/* Cards */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid var(--border-color);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

/* Form controls */
.form-control {
    background-color: var(--card-bg);
    border-color: var(--border-color);
    color: white;
}

.form-control:focus {
    background-color: var(--card-bg);
    border-color: var(--primary-purple);
    color: white;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.form-select {
    background-color: var(--card-bg);
    border-color: var(--border-color);
    color: white;
}

/* Alerts */
.alert {
    border: none;
    border-radius: 10px;
}

/* Progress indicators */
.progress {
    background-color: var(--card-bg);
}

.progress-bar {
    background-color: var(--primary-purple);
}

/* Loading spinner */
.spinner-border-purple {
    color: var(--primary-purple);
}

/* Custom animations */
@keyframes pulse {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
    100% {
        transform: scale(1);
    }
}

.pulse-animation {
    animation: pulse 2s infinite;
}

/* Responsive typography */
@media (max-width: 768px) {
    .display-4 {
        font-size: 2.5rem;
    }
    
    .display-5 {
        font-size: 2rem;
    }
    
    .lead {
        font-size: 1.1rem;
    }
}

/* Dashboard specific styles */
.dashboard-card {
    background: linear-gradient(135deg, var(--card-bg) 0%, #3a3a3a 100%);
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.dashboard-card:hover {
    border-color: var(--primary-purple);
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
}

/* Status badges */
.badge {
    font-size: 0.8rem;
    padding: 0.5em 0.8em;
}

.badge.bg-pending {
    background-color: #ffc107 !important;
    color: #000;
}

.badge.bg-enrolled {
    background-color: #28a745 !important;
}

.badge.bg-completed {
    background-color: #17a2b8 !important;
}

.badge.bg-cancelled {
    background-color: #dc3545 !important;
}

/* Star rating styles */
.star-rating {
    display: flex;
    gap: 5px;
    margin-bottom: 10px;
}

.star-rating i {
    font-size: 24px;
    color: #6c757d;
    cursor: pointer;
    transition: all 0.2s ease;
}

.star-rating i:hover,
.star-rating i.active {
    color: #ffc107;
    transform: scale(1.1);
}

/* Modal customizations */
.modal-content {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
}

.modal-header {
    border-bottom-color: var(--border-color);
}

.modal-footer {
    border-top-color: var(--border-color);
}

/* Table styles */
.table-dark {
    --bs-table-bg: var(--card-bg);
    --bs-table-border-color: var(--border-color);
}

/* Course listing styles */
.course-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 15px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.course-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    border-color: var(--primary-purple);
}

.course-card img {
    height: 200px;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.course-card:hover img {
    transform: scale(1.05);
}

.course-price {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-purple);
}

/* Timeline styles for about page */
.timeline {
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
}

.timeline::after {
    content: '';
    position: absolute;
    width: 6px;
    background-color: var(--primary-purple);
    top: 0;
    bottom: 0;
    left: 50%;
    margin-left: -3px;
}

.timeline-item {
    padding: 10px 40px;
    position: relative;
    background-color: inherit;
    width: 50%;
}

.timeline-item::after {
    content: '';
    position: absolute;
    width: 25px;
    height: 25px;
    right: -17px;
    background-color: var(--primary-purple);
    border: 4px solid var(--dark-bg);
    top: 15px;
    border-radius: 50%;
    z-index: 1;
}

.timeline-item:nth-child(even) {
    left: 50%;
}

.timeline-item:nth-child(even)::after {
    left: -16px;
}

.timeline-content {
    padding: 20px 30px;
    background-color: var(--card-bg);
    position: relative;
    border-radius: 6px;
    border: 1px solid var(--border-color);
}

/* Certificate styles */
.certificate-preview {
    border: 3px solid var(--primary-purple);
    border-radius: 15px;
    padding: 2rem;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    color: #000;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.certificate-title {
    font-family: 'Georgia', serif;
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--primary-purple);
    margin-bottom: 1rem;
}

.certificate-student-name {
    font-size: 2rem;
    font-weight: bold;
    color: #333;
    margin: 1rem 0;
}

/* Payment form styles */
.payment-summary {
    background: linear-gradient(135deg, var(--primary-purple) 0%, var(--secondary-purple) 100%);
    color: white;
    border-radius: 15px;
    padding: 2rem;
    margin-bottom: 2rem;
}

.bank-account-display {
    background: #fff;
    color: #000;
    padding: 1.5rem;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    border: 3px dashed var(--primary-purple);
    margin: 1rem 0;
}

.session-timer {
    background: linear-gradient(45deg, #ff6b6b, #ffa500);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    font-size: 1.2rem;
    font-weight: bold;
    animation: pulse 2s infinite;
}

/* Media resource styles */
.media-resource-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 15px;
    overflow: hidden;
    transition: all 0.3s ease;
    height: 100%;
}

.media-resource-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    border-color: var(--primary-purple);
}

.resource-type-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    z-index: 2;
}

.video-thumbnail {
    position: relative;
    overflow: hidden;
}

.video-thumbnail::before {
    content: '\f04b';
    font-family: 'Font Awesome 6 Free';
    font-weight: 900;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 3rem;
    color: white;
    z-index: 2;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.video-thumbnail:hover::before {
    opacity: 1;
}

.video-thumbnail::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.video-thumbnail:hover::after {
    opacity: 1;
}

/* Event card styles */
.event-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 15px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.event-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    border-color: var(--primary-purple);
}

.event-date {
    background: var(--primary-purple);
    color: white;
    padding: 1rem;
    text-align: center;
    font-weight: bold;
}

.event-type-badge {
    background: var(--secondary-purple);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Testimonial styles */
.testimonial-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 15px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.testimonial-card::before {
    content: '"';
    position: absolute;
    top: -20px;
    left: 20px;
    font-size: 8rem;
    color: var(--primary-purple);
    opacity: 0.2;
    font-family: 'Georgia', serif;
}

.testimonial-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    border-color: var(--primary-purple);
}

.testimonial-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 3px solid var(--primary-purple);
    object-fit: cover;
    margin: 0 auto 1rem;
}

.testimonial-stars {
    color: #ffc107;
    font-size: 1.2rem;
    margin-bottom: 1rem;
}

/* Loading states */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.loading-spinner {
    width: 50px;
    height: 50px;
    border: 5px solid var(--border-color);
    border-top: 5px solid var(--primary-purple);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Error states */
.error-page {
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.error-code {
    font-size: 8rem;
    font-weight: bold;
    color: var(--primary-purple);
    line-height: 1;
}

/* Success states */
.success-checkmark {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: block;
    stroke-width: 2;
    stroke: #28a745;
    stroke-miterlimit: 10;
    margin: 10% auto;
    box-shadow: inset 0px 0px 0px #28a745;
    animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
}

.success-checkmark-circle {
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: 2;
    stroke-miterlimit: 10;
    stroke: #28a745;
    fill: none;
    animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.success-checkmark-check {
    transform-origin: 50% 50%;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}

@keyframes stroke {
    100% {
        stroke-dashoffset: 0;
    }
}

@keyframes scale {
    0%, 100% {
        transform: none;
    }
    50% {
        transform: scale3d(1.1, 1.1, 1);
    }
}

@keyframes fill {
    100% {
        box-shadow: inset 0px 0px 0px 30px #28a745;
    }
}

/* Print styles */
@media print {
    .navbar,
    .footer,
    .btn,
    .no-print {
        display: none !important;
    }
    
    body {
        background: white !important;
        color: black !important;
    }
    
    .card {
        border: 1px solid #ccc !important;
        background: white !important;
    }
}

/* Dark mode toggle */
.dark-mode-toggle {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 25px;
    padding: 0.5rem 1rem;
    color: white;
    transition: all 0.3s ease;
}

.dark-mode-toggle:hover {
    background: var(--primary-purple);
    color: white;
}

/* Accessibility improvements */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

.focus-visible {
    outline: 2px solid var(--primary-purple);
    outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    :root {
        --primary-purple: #0066cc;
        --secondary-purple: #004499;
        --border-color: #666;
    }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
"""

# celery.py (Root level)
"""
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ultima_training.settings')

app = Celery('ultima_training')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
"""

# manage.py
"""
#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ultima_training.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
"""

# Dockerfile
"""
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create media directory
RUN mkdir -p media

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ultima_training.wsgi:application"]
"""

# docker-compose.yml
"""
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ultima_training
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DEBUG=True
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0

  celery:
    build: .
    command: celery -A ultima_training worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DEBUG=True
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0

  celery-beat:
    build: .
    command: celery -A ultima_training beat --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DEBUG=True
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0

volumes:
  postgres_data:
"""

# .env.example
"""
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=ultima_training
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=admin@ultimatraining.com

# Payment settings
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# Security settings (for production)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
"""

# Installation and Setup Instructions
"""
# ULTIMA TRAINING PLATFORM - SETUP INSTRUCTIONS

## Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Node.js 16+ (for frontend assets)

## Installation Steps

1. Clone the repository:
   git clone <repository-url>
   cd ultima-training-platform

2. Create virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Setup environment variables:
   cp .env.example .env
   # Edit .env with your settings

5. Setup database:
   createdb ultima_training
   python manage.py migrate

6. Create superuser:
   python manage.py createsuperuser

7. Collect static files:
   python manage.py collectstatic

8. Load initial data (optional):
   python manage.py loaddata fixtures/initial_data.json

9. Start Redis (in another terminal):
   redis-server

10. Start Celery worker (in another terminal):
    celery -A ultima_training worker --loglevel=info

11. Start Celery beat scheduler (in another terminal):
    celery -A ultima_training beat --loglevel=info

12. Run development server:
    python manage.py runserver

## Docker Setup (Alternative)

1. Clone repository and navigate to directory

2. Build and run with Docker Compose:
   docker-compose up --build

3. Run migrations:
   docker-compose exec web python manage.py migrate

4. Create superuser:
   docker-compose exec web python manage.py createsuperuser

## Production Deployment

1. Set environment variables for production
2. Configure nginx for static file serving
3. Use gunicorn with supervisor for process management
4. Setup SSL certificate
5. Configure backup strategy for database and media files

## Features Overview

### Student Features:
- User registration and authentication
- Course browsing and registration
- Payment processing (PayPal/Iranian banking)
- Dashboard with course management
- Feedback submission
- Certificate download
- Course cancellation with refund requests

### Instructor Features:
- Student approval/rejection
- Course management
- Feedback review and approval
- Certificate generation approval

### Admin Features:
- Complete course management
- Instructor management
- Student data access
- Analytics and reporting

### Dr. Josef Balahan Branding:
- Personal brand homepage
- About page with timeline
- Events and workshops listing
- Testimonials showcase
- Media resources library
- Contact and speaking request forms

### Technical Features:
- Responsive design (mobile-first)
- Dark theme with purple accents
- Real-time notifications
- Email automation
- PDF certificate generation
- QR code verification
- Payment webhook handling
- Session management
- Error handling and logging

## API Endpoints

### Authentication:
- POST /accounts/register/ - Student registration
- POST /accounts/login/ - User login
- POST /accounts/logout/ - User logout

### Courses:
- GET /courses/ - List courses
- GET /courses/{id}/ - Course details
- POST /courses/{id}/register/ - Register for course
- POST /courses/enrollment/{id}/cancel/ - Cancel enrollment

### Payments:
- POST /payments/process/{enrollment_id}/ - Process payment
- POST /payments/iranian/{payment_id}/complete/ - Complete Iranian payment
- POST /payments/webhooks/paypal/ - PayPal webhook

### Certificates:
- GET /certificates/download/{id}/ - Download certificate
- GET /certificates/verify/{number}/ - Verify certificate

## Security Considerations

- CSRF protection enabled
- SQL injection prevention
- XSS protection
- Secure password hashing
- Rate limiting on forms
- File upload restrictions
- Session security
- HTTPS enforcement in production

## Performance Optimizations

- Database query optimization
- Redis caching
- Static file compression
- Image optimization
- Celery for background tasks
- Database connection pooling
- CDN integration ready

## Monitoring and Logging

- Django logging configuration
- Celery task monitoring
- Error tracking setup
- Performance monitoring
- Database query logging
- User activity tracking

## Backup Strategy

- Automated database backups
- Media file backups
- Environment configuration backups
- SSL certificate backups
- Application code version control

This platform provides a complete, production-ready solution for the Ultima Training educational platform with all the specified features and workflows.
"""