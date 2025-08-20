
# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name='student_register'),
    path('profile/', views.profile_view, name='profile'),
]
