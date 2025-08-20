from django.contrib import admin
from .models import Testimonial, MediaResource, Event

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course', 'rating', 'is_approved')
    list_filter = ('is_approved', 'is_featured')

@admin.register(MediaResource)
class MediaResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'is_public')
    list_filter = ('resource_type', 'is_public')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_datetime')
    list_filter = ('event_type', 'is_past_event')