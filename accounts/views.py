
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
