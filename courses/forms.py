# courses/forms.py
from django import forms
from .models import Enrollment, Feedback, CourseSession
from django.utils import timezone

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