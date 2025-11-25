from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    Otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    # Assistant executive flag: users with this flag can review bookings
    is_assistant_executive = models.BooleanField(default=False)
    # Client flag: all verified users are clients by default
    is_client = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    




class Car(models.Model):
    TYPE_CHOICES = [
        ('rent', 'Rent'),
        ('sale', 'Sale'),
    ]

    model = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True, null=True, unique=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='cars/', blank=True, null=True)
    car_type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='rent')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")

    def __str__(self):
        return f"{self.model} ({self.get_car_type_display()})"

    def price_display(self):
        """
        Return a display-friendly price string (template helper).
        """
        if self.car_type == 'rent':
            return f"Per Hour {self.price} / day"
        return f" BDT {self.price}"


class Booking(models.Model):
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True, blank=True)
    # Who created the booking (nullable for anonymous flows)
    requester = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='bookings')
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    id_number = models.CharField(max_length=100, help_text='NID or Passport number')
    driving_license_number = models.CharField(max_length=100, blank=True)
    driving_license_photo = models.ImageField(upload_to='bookings/licenses/', blank=True, null=True)
    client_photo = models.ImageField(upload_to='bookings/clients/', blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Request type: rent or buy
    REQUEST_TYPE_CHOICES = [
        ('rent', 'Rent'),
        ('buy', 'Buy'),
        ('cancel', 'Cancel Request'),
    ]
    request_type = models.CharField(max_length=12, choices=REQUEST_TYPE_CHOICES, default='rent')

    # Status flow for booking
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('cancel_requested', 'Cancel Requested'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Who processed (confirmed/rejected) the booking
    processed_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='processed_bookings')
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Track delivery completion
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.full_name} ({self.mobile}) - {self.car_id or 'No car'}"
