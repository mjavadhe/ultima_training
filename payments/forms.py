# payments/forms.py
from django import forms
from .models import Refund

class IranianPaymentForm(forms.Form):
    rahgiri_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Rahgiri Code',
            'required': True
        })
    )

class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['amount', 'reason', 'bank_card_number', 'cardholder_name']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bank_card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last 4 digits only'}),
            'cardholder_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        payment = kwargs.pop('payment', None)
        super().__init__(*args, **kwargs)
        
        if payment:
            self.fields['amount'].initial = payment.amount
            
            # Show Iranian-specific fields only for Iranian payments
            if payment.payment_method != 'bank_transfer':
                del self.fields['bank_card_number']
                del self.fields['cardholder_name']
