from django.contrib import admin
from .models import Car
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.


admin.site.register(CustomUser)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'car_type', 'price', 'available', 'created_at')
    list_filter = ('car_type', 'available', 'created_at')
    search_fields = ('model', 'description')
    readonly_fields = ('created_at',)