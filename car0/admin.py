from django.contrib import admin

# Register your models here.
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'car_type', 'price', 'available', 'created_at')
    list_filter = ('car_type', 'available', 'created_at')
    search_fields = ('model', 'description')
    readonly_fields = ('created_at',)