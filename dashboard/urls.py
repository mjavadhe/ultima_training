# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]