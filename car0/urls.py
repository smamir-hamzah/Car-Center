
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/car/<int:id>/', api_car, name='api_car'),
    path('signup/', signup_view, name='signup'),
    path('otp/', otp_verify, name='otp_verify'),
    path('car/<int:car_id>/', car_detail, name='car_detail'),
    path('usercar/<int:car_id>/', usercar_detail, name='usercar_detail'),
    path('book/', booking_view, name='book'),
    path('book/<int:booking_id>/cancel-request/', booking_cancel_request, name='booking_cancel_request'),
    path('assistant/', assistant_dashboard, name='assistant_dashboard'),
    path('assistant/process/<int:booking_id>/', assistant_process_booking, name='assistant_process_booking'),
    path('assistant/mark-complete/<int:booking_id>/', mark_delivery_complete, name='mark_delivery_complete'),
    path('assistant/approve-cancel/<int:booking_id>/', cancel_booking_confirmed, name='cancel_booking_confirmed'),
    path('assistant/deny-cancel/<int:booking_id>/', deny_cancellation, name='deny_cancellation'),
    path('review/submit/', submit_review, name='submit_review'),
    path('userhtml/', userhtml, name='userhtml'),
]
