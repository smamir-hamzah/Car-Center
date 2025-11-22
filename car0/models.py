from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    Otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_passenger = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    


from django.db import models
from django.utils.translation import gettext_lazy as _

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
            return f"${self.price} / day"
        return f"${self.price}"
