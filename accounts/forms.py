
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'middle_name', 'last_name', 
                 'mobile', 'country_code', 'organization', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'country_code': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country_code'].choices = [
            ('+1', 'United States (+1)'),
            ('+44', 'United Kingdom (+44)'),
            ('+49', 'Germany (+49)'),
            ('+33', 'France (+33)'),
            ('+98', 'Iran (+98)'),
            ('+971', 'UAE (+971)'),
            ('+966', 'Saudi Arabia (+966)'),
        ]
        self.fields['middle_name'].required = False
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'mobile', 
                 'country_code', 'organization', 'profile_picture', 'bio')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'country_code': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# courses/forms.py
from django import forms
from .models import Enrollment, Feedback, CourseSession

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
