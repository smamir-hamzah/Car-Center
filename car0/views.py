from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Car, Booking
from django.shortcuts import redirect

import random
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.utils import timezone




def home(request):
    rentCars = Car.objects.filter(car_type='rent', available=True)[:50]
    saleCars = Car.objects.filter(car_type='sale', available=True)[:50]

    # Example reviews for template rendering (you can replace with a Review model later)
    reviews = [
        {"text": "Great service and clean cars.", "name": "Aisha", "rating": 5},
        {"text": "Smooth booking experience.", "name": "Rafi", "rating": 4},
        {"text": "Helpful staff and quick pickup.", "name": "Tania", "rating": 5},
    ]

    context = {
        "rentCars": rentCars,
        "saleCars": saleCars,
        "reviews": reviews,
    }
    return render(request, "home.html", context)


def api_car(request, id):
    car = get_object_or_404(Car, pk=id)
    data = {
        "id": car.id,
        "title": car.model,
        "description": car.description,
        "price": str(car.price_display()) if hasattr(car, "price_display") else str(car.price),
        "image": car.photo.url if car.photo else "",
        "type": car.car_type,
    }
    return JsonResponse(data)


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car-details.html', {'car': car})


def usercar_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'usercar_detail.html', {'car': car})




def booking_view(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id') or None
        car = None
        if car_id:
            try:
                car = Car.objects.get(id=car_id)
            except Car.DoesNotExist:
                car = None
        full_name = request.POST.get('full_name')
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')
        id_number = request.POST.get('id_number')
        driving_license_number = request.POST.get('driving_license_number')
        request_type = request.POST.get('request_type') or 'rent'

        booking = Booking.objects.create(
            car=car,
            requester=request.user if request.user.is_authenticated else None,
            full_name=full_name or '',
            mobile=mobile or '',
            location=location or '',
            id_number=id_number or '',
            driving_license_number=driving_license_number or '',
            request_type=request_type,
            status='pending',
        )

        if request.FILES.get('driving_license_photo'):
            booking.driving_license_photo = request.FILES['driving_license_photo']
        if request.FILES.get('client_photo'):
            booking.client_photo = request.FILES['client_photo']
        booking.save()
        # If it's a cancel request initiated by the user, notify staff
        if booking.request_type == 'cancel':
            notify_staff_cancel_request(booking)

        return render(request, 'booking_success.html', {'booking': booking})

    # fallback redirect
    return redirect('home')


def userhtml(request):
    rentCars = Car.objects.filter(car_type='rent', available=True)[:50]
    saleCars = Car.objects.filter(car_type='sale', available=True)[:50]
    reviews = [
        {"text": "Great service and clean cars.", "name": "Aisha", "rating": 5},
        {"text": "Smooth booking experience.", "name": "Rafi", "rating": 4},
        {"text": "Helpful staff and quick pickup.", "name": "Tania", "rating": 5},
    ]

    focus_car = request.GET.get('from_car')
    try:
        focus_car_id = int(focus_car) if focus_car else None
    except (TypeError, ValueError):
        focus_car_id = None

    # Get user's bookings if logged in
    my_bookings = []
    if request.user.is_authenticated:
        my_bookings = Booking.objects.filter(requester=request.user).order_by('-created_at')

    context = {
        "rentCars": rentCars,
        "saleCars": saleCars,
        "reviews": reviews,
        "focus_car_id": focus_car_id,
        "my_bookings": my_bookings,
    }
    return render(request, 'user.html', context)




# Login and Signup Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Bypass verification for admin users
            if not user.is_superuser and not user.is_verified:
                messages.warning(request, 'Account not verified — please verify your email')
                return redirect('login')

            login(request, user)

            # Role-based redirects
            if user.is_superuser and user.is_staff:
                return redirect('admin:index')
            elif user.is_assistant_executive:
                return redirect('assistant_dashboard')
            else:
                return redirect('userhtml')

        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    return render(request, 'login.html')


def signup_view(request):
    """Register new user with OTP verification"""
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')

        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')

        # Generate OTP
        otp = f"{random.randint(10000, 99999):05d}"

        # Create user (not verified yet)
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
            image=image,
            Otp=otp,
            is_verified=False
        )

        # Send OTP email
        try:
            send_otp_email(otp, email, username)
            messages.success(request, 'Account created — check your email for OTP verification')
            request.session['otp_email'] = email
            return redirect('otp_verify')
        except Exception as e:
            user.delete()
            messages.error(request, f'Failed to send OTP: {str(e)}')
            return redirect('signup')

    return render(request, 'signup.html')


def send_otp_email(otp, email, username):
    """Send OTP verification email"""
    subject = 'AutoWave — Your OTP for Account Verification'
    message_body = f'''
Hello {username},

Your One-Time Password (OTP) for AutoWave account verification is:

    {otp}

This OTP will expire in 10 minutes. Please do not share this code with anyone.

If you did not request this code, please ignore this email.

Best regards,
AutoWave Team
'''
    from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@autowave.com'
    send_mail(subject, message_body, from_email, [email], fail_silently=False)


def otp_verify(request):
    """Verify OTP and activate user account"""
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        email = request.session.get('otp_email')

        if not email:
            messages.error(request, 'Session expired — please sign up again')
            return redirect('signup')

        try:
            user = CustomUser.objects.get(email=email)
            if user.Otp == otp_code:
                user.is_verified = True
                user.is_client = True
                user.save()
                messages.success(request, 'Email verified — you can now login')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP — please try again')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found')

    return render(request, 'otp_verify.html')


def logout_view(request):
    """Logout user and redirect to login page"""
    logout(request)
    return redirect('login')


def notify_staff_cancel_request(booking):
    """Send email notification about a cancel request to admins and assistant executives."""
    subject = f"Cancel request for booking #{booking.id}"
    body = f"Booking #{booking.id} by {booking.full_name} (mobile: {booking.mobile}) has requested cancellation.\n\nPlease review and confirm or reject the cancellation in the assistant dashboard.\n"
    from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@autowave.com'

    # collect recipients: admins and assistant executives
    admins = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
    assistants = CustomUser.objects.filter(is_assistant_executive=True).values_list('email', flat=True)
    recipients = set(list(admins) + list(assistants))
    recipients = [r for r in recipients if r]
    if recipients:
        send_mail(subject, body, from_email, recipients, fail_silently=True)


@login_required
def assistant_dashboard(request):
    # Only assistant executives and staff can view
    if not (request.user.is_superuser or request.user.is_assistant_executive):
        messages.error(request, 'Permission denied')
        return redirect('home')

    # Show only pending and cancel_requested bookings (not completed ones)
    rent_requests = Booking.objects.filter(request_type='rent', status='pending', is_completed=False).order_by('-created_at')
    buy_requests = Booking.objects.filter(request_type='buy', status='pending', is_completed=False).order_by('-created_at')
    cancel_requests = Booking.objects.filter(status='cancel_requested', is_completed=False).order_by('-created_at')
    
    # Show confirmed bookings awaiting delivery completion
    confirmed_bookings = Booking.objects.filter(status='confirmed', is_completed=False).order_by('-created_at')

    return render(request, 'assistant_dashboard.html', {
        'rent_requests': rent_requests,
        'buy_requests': buy_requests,
        'cancel_requests': cancel_requests,
        'confirmed_bookings': confirmed_bookings,
    })


@login_required
def assistant_process_booking(request, booking_id):
    # Process confirm/reject actions from assistant dashboard
    if not (request.user.is_superuser or request.user.is_assistant_executive):
        messages.error(request, 'Permission denied')
        return redirect('home')

    booking = get_object_or_404(Booking, id=booking_id)
    action = request.POST.get('action')
    
    if action == 'confirm':
        booking.status = 'confirmed'
        booking.processed_by = request.user
        booking.processed_at = timezone.now()
        booking.save()
        messages.success(request, f'Booking #{booking.id} confirmed')
        
        # Send confirmation email to requester
        if booking.requester and booking.requester.email:
            try:
                send_mail(
                    f'Your booking #{booking.id} has been confirmed',
                    f'Hello {booking.full_name},\n\nYour booking for {booking.car.model if booking.car else "the requested car"} has been confirmed.\n\nBooking Details:\n- Type: {booking.get_request_type_display()}\n- ID: #{booking.id}\n- Mobile: {booking.mobile}\n\nPlease visit our office to complete the process.\n\nBest regards,\nAutoWave Team',
                    settings.DEFAULT_FROM_EMAIL or 'noreply@autowave.com',
                    [booking.requester.email],
                    fail_silently=True
                )
            except Exception:
                pass
                
    elif action == 'reject':
        booking.status = 'rejected'
        booking.processed_by = request.user
        booking.processed_at = timezone.now()
        booking.save()
        messages.success(request, f'Booking #{booking.id} rejected and requester notified')
        
        # Send rejection email to requester
        try:
            if booking.requester and booking.requester.email:
                send_mail(
                    f'Your booking #{booking.id} was rejected',
                    f'Hello {booking.full_name},\n\nUnfortunately, your booking for {booking.car.model if booking.car else "the requested car"} has been rejected.\n\nBooking ID: #{booking.id}\n\nPlease contact support for more information or to submit a new booking.\n\nBest regards,\nAutoWave Team',
                    settings.DEFAULT_FROM_EMAIL or 'noreply@autowave.com',
                    [booking.requester.email],
                    fail_silently=True
                )
        except Exception:
            pass

    return redirect('assistant_dashboard')


@login_required
def booking_cancel_request(request, booking_id):
    # User requests cancellation of an existing booking
    booking = get_object_or_404(Booking, id=booking_id)
    # Only the requester or staff can request cancellation
    if not (request.user == booking.requester or request.user.is_superuser or request.user.is_assistant_executive):
        messages.error(request, 'Permission denied')
        return redirect('userhtml')

    booking.status = 'cancel_requested'
    booking.save()
    notify_staff_cancel_request(booking)
    messages.success(request, 'Cancellation requested — staff will review')
    return redirect('userhtml')


@login_required
def mark_delivery_complete(request, booking_id):
    """
    Admin or Assistant marks a confirmed booking as delivery complete.
    This will hide the booking from assistant view and update user's booking status.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only admin or assistant can mark as complete
    if not (request.user.is_superuser or request.user.is_assistant_executive):
        messages.error(request, 'Permission denied')
        return redirect('userhtml')
    
    # Can only mark confirmed bookings as complete
    if booking.status != 'confirmed':
        messages.error(request, 'Only confirmed bookings can be marked as complete')
        return redirect('assistant_dashboard')
    
    booking.is_completed = True
    booking.status = 'completed'
    booking.save()
    
    # Send completion email to requester
    if booking.requester and booking.requester.email:
        try:
            send_mail(
                f'Your booking #{booking.id} delivery is complete',
                f'Hello {booking.full_name},\n\nYour booking delivery is complete!\n\nBooking Details:\n- Type: {booking.get_request_type_display()}\n- ID: #{booking.id}\n- Car: {booking.car.model if booking.car else "N/A"}\n\nThank you for choosing AutoWave!\n\nBest regards,\nAutoWave Team',
                settings.DEFAULT_FROM_EMAIL or 'noreply@autowave.com',
                [booking.requester.email],
                fail_silently=True
            )
        except Exception:
            pass
    
    messages.success(request, f'Booking #{booking.id} marked as complete')
    return redirect('assistant_dashboard')


@login_required
def cancel_booking_confirmed(request, booking_id):
    """
    Admin or Assistant confirms/approves a cancellation request.
    Updates booking status to 'cancelled' and notifies user.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only admin or assistant can approve cancellation
    if not (request.user.is_superuser or request.user.is_assistant_executive):
        messages.error(request, 'Permission denied')
        return redirect('userhtml')
    
    # Can only approve cancel_requested bookings
    if booking.status != 'cancel_requested':
        messages.error(request, 'Invalid booking status for cancellation')
        return redirect('assistant_dashboard')
    
    booking.status = 'cancelled'
    booking.is_completed = True
    booking.save()
    
    # Send cancellation approval email to requester
    if booking.requester and booking.requester.email:
        try:
            send_mail(
                f'Your booking #{booking.id} cancellation has been approved',
                f'Hello {booking.full_name},\n\nYour cancellation request has been approved.\n\nBooking ID: #{booking.id}\n- Status: Cancelled\n\nThank you for using AutoWave!\n\nBest regards,\nAutoWave Team',
                settings.DEFAULT_FROM_EMAIL or 'noreply@autowave.com',
                [booking.requester.email],
                fail_silently=True
            )
        except Exception:
            pass
    
    messages.success(request, f'Booking #{booking.id} cancellation approved')
    return redirect('assistant_dashboard')


@login_required
def deny_cancellation(request, booking_id):
    """
    Admin or Assistant denies a cancellation request.
    Booking reverts to 'confirmed' status and notifies user.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only admin or assistant can deny cancellation
    if not (request.user.is_superuser or request.user.is_assistant_executive):
        messages.error(request, 'Permission denied')
        return redirect('userhtml')
    
    # Can only deny cancel_requested bookings
    if booking.status != 'cancel_requested':
        messages.error(request, 'Invalid booking status for cancellation denial')
        return redirect('assistant_dashboard')
    
    booking.status = 'confirmed'
    booking.save()
    
    # Send cancellation denial email to requester
    if booking.requester and booking.requester.email:
        try:
            send_mail(
                f'Your booking #{booking.id} cancellation request was denied',
                f'Hello {booking.full_name},\n\nYour cancellation request has been denied.\n\nYour booking remains active:\n- Booking ID: #{booking.id}\n- Status: Confirmed\n- Car: {booking.car.model if booking.car else "N/A"}\n\nIf you have questions, please contact support.\n\nBest regards,\nAutoWave Team',
                settings.DEFAULT_FROM_EMAIL or 'noreply@autowave.com',
                [booking.requester.email],
                fail_silently=True
            )
        except Exception:
            pass
    
    messages.success(request, f'Booking #{booking.id} cancellation denied')
    return redirect('assistant_dashboard')
