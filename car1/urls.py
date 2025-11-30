from django.urls import path
from . views import *
urlpatterns = [
    path('contact/', contact_us, name='contact_us'),
]
