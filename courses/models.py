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