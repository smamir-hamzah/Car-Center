from django.contrib import admin
from .models import Car
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Booking
from .models import Review

# Register your models here.


admin.site.register(CustomUser)



@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'car_type', 'price', 'available', 'created_at')
    list_filter = ('car_type', 'available', 'created_at')
    search_fields = ('model', 'description')
    readonly_fields = ('created_at',)

    def price_display(self, obj):
        return obj.price_display()
    



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'requester', 'full_name', 'mobile', 'request_type', 'status', 'created_at')
    list_filter = ('status', 'request_type', 'created_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'text')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('full_name', 'mobile', 'id_number', 'car__model')
    readonly_fields = ('created_at',)
    # # Show all fields except created_at as editable
    # fields = [
    #     'car', 'requester', 'full_name', 'mobile', 'location', 'id_number', 'driving_license_number',
    #     'driving_license_photo', 'client_photo', 'request_type', 'status', 'processed_by', 'processed_at',
    #     'is_completed'
    # ]
    def is_completed(self, obj):
        return obj.status == 'completed'
