from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Car, Booking
from django.shortcuts import redirect

def home(request):
    """
    Render home page with two lists: rentCars and saleCars.
    """
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
    """
    JSON endpoint used by JS details page. Returns 404 JSON if not found.
    """
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


def login_view(request):
    if request.method == "POST":
        # your login logic
        pass

    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        # Placeholder for signup logic (e.g., create user)
        # name = request.POST.get('name')
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # Add your user creation logic here
        return render(request, 'signup_success.html')  # Or redirect as needed
    return render(request, 'signup.html')

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

        booking = Booking.objects.create(
            car=car,
            full_name=full_name or '',
            mobile=mobile or '',
            location=location or '',
            id_number=id_number or '',
            driving_license_number=driving_license_number or '',
        )

        # handle files
        if request.FILES.get('driving_license_photo'):
            booking.driving_license_photo = request.FILES['driving_license_photo']
        if request.FILES.get('client_photo'):
            booking.client_photo = request.FILES['client_photo']
        booking.save()

        return render(request, 'booking_success.html', {'booking': booking})

    # fallback redirect
    return redirect('home')


def userhtml(request):
    """Render user page with two lists: rentCars and saleCars.
    If the user came from a car details page, a query param `from_car` may
    be provided so the template can focus that car (show only the relevant
    action button).
    """
    rentCars = Car.objects.filter(car_type='rent', available=True)[:50]
    saleCars = Car.objects.filter(car_type='sale', available=True)[:50]

    # Example reviews for template rendering (you can replace with a Review model later)
    reviews = [
        {"text": "Great service and clean cars.", "name": "Aisha", "rating": 5},
        {"text": "Smooth booking experience.", "name": "Rafi", "rating": 4},
        {"text": "Helpful staff and quick pickup.", "name": "Tania", "rating": 5},
    ]

    # focus_car_id is an optional integer from ?from_car=<id>
    focus_car = request.GET.get('from_car')
    try:
        focus_car_id = int(focus_car) if focus_car else None
    except (TypeError, ValueError):
        focus_car_id = None

    context = {
        "rentCars": rentCars,
        "saleCars": saleCars,
        "reviews": reviews,
        "focus_car_id": focus_car_id,
    }
    return render(request, 'user.html', context)