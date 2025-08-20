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