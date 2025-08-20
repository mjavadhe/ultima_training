# branding/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from courses.models import Course

User = get_user_model()

class Testimonial(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials', db_index=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='testimonials', db_index=True)
    
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
    
    def save(self, *args, **kwargs):
        self.student_name = self.student.get_full_name()
        super().save(*args, **kwargs)

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