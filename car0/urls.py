
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('api/car/<int:id>/', api_car, name='api_car'),
    path('signup/', signup_view, name='signup'),
    path('car/<int:car_id>/', car_detail, name='car_detail'),
    path('usercar/<int:car_id>/', usercar_detail, name='usercar_detail'),
    path('usercar/<int:car_id>/', usercar_detail, name='usercar_detail'),
    path('book/', booking_view, name='book'),
    path('userhtml/', userhtml, name='userhtml'),
]
