
from django.urls import path
from .views import home, api_car, login_view, signup_view , car_detail

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('api/car/<int:id>/', api_car, name='api_car'),
    path('signup/', signup_view, name='signup'),
    path('car/<int:car_id>/', car_detail, name='car_detail'),
]
