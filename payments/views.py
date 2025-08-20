
# payments/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from courses.models import Enrollment
from .models import Payment
from .forms import IranianPaymentForm

@login_required
def payment_process(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        student=request.user,
        status='pending'
    )
    
    # Check if payment already exists
    try:
        payment = enrollment.payment
        if payment.status == 'completed':
            messages.info(request, 'Payment already completed.')
            return redirect('student_dashboard')
    except Payment.DoesNotExist:
        # Create new payment record
        payment = Payment.objects.create(
            enrollment=enrollment,
            amount=enrollment.final_price,
            currency=enrollment.course.currency,
            payment_method='paypal' if not request.user.is_iranian else 'bank_transfer'
        )
    
    context = {
        'enrollment': enrollment,
        'payment': payment,
        'is_iranian': request.user.is_iranian,
    }
    
    if request.user.is_iranian:
        return render(request, 'payments/iranian_payment.html', context)
    else:
        return render(request, 'payments/international_payment.html', context)

@login_required
@csrf_exempt
def iranian_payment_complete(request, payment_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    payment = get_object_or_404(Payment, id=payment_id, enrollment__student=request.user)
    
    form = IranianPaymentForm(request.POST)
    if form.is_valid():
        rahgiri_code = form.cleaned_data['rahgiri_code']
        
        # Validate Rahgiri code (implement your validation logic)
        if validate_rahgiri_code(rahgiri_code, payment.amount):
            payment.rahgiri_code = rahgiri_code
            payment.status = 'completed'
            payment.payment_date = timezone.now()
            payment.save()
            
            # Update enrollment status
            payment.enrollment.status = 'enrolled'
            payment.enrollment.save()
            
            # Send confirmation email
            from .tasks import send_payment_confirmation_email
            send_payment_confirmation_email.delay(payment.id)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Payment completed successfully!',
                'redirect_url': '/dashboard/'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid Rahgiri code. Please check and try again.'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Please provide a valid Rahgiri code.'
    })

def validate_rahgiri_code(rahgiri_code, amount):
    """
    Implement your Rahgiri code validation logic here
    This should connect to the Iranian banking system API
    """
    # Placeholder implementation
    return len(rahgiri_code) >= 10

@csrf_exempt
def paypal_webhook(request):
    """Handle PayPal webhook notifications"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        event_type = data.get('event_type')
        
        if event_type == 'PAYMENT.CAPTURE.COMPLETED':
            # Extract payment information
            payment_id = data['resource']['id']
            amount = float(data['resource']['amount']['value'])
            
            # Find corresponding payment
            try:
                payment = Payment.objects.get(
                    transaction_id=payment_id,
                    payment_method='paypal'
                )
                payment.status = 'completed'
                payment.payment_date = timezone.now()
                payment.save()
                
                # Update enrollment
                payment.enrollment.status = 'enrolled'
                payment.enrollment.save()
                
                # Send confirmation email
                from .tasks import send_payment_confirmation_email
                send_payment_confirmation_email.delay(payment.id)
                
            except Payment.DoesNotExist:
                pass
        
        return JsonResponse({'status': 'success'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
