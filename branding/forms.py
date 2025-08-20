# branding/forms.py
from django import forms

class ContactForm(forms.Form):
    PURPOSE_CHOICES = [
        ('speaking', 'Speaking Request'),
        ('corporate', 'Corporate Training'),
        ('general', 'General Inquiry'),
    ]
    
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    company = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    purpose = forms.ChoiceField(choices=PURPOSE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

class SpeakingRequestForm(forms.Form):
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('corporate', 'Corporate Event'),
        ('webinar', 'Webinar'),
    ]
    
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    company = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    event_type = forms.ChoiceField(choices=EVENT_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))
    event_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    audience_size = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    budget_range = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    topics = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    additional_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
