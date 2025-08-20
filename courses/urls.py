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
