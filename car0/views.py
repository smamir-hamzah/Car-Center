from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Car

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