# branding/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at').prefetch_related('student', 'course')
    
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
            from .tasks import send_speaking_request_notification
            send_speaking_request_notification.delay(form.cleaned_data)
            messages.success(request, 'Your speaking request has been submitted successfully!')
            return redirect('homepage')
    else:
        form = SpeakingRequestForm()
    
    context = {'form': form}
    return render(request, 'branding/speaking_request.html', context)