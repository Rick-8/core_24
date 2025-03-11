# bookings/admin.py

from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date']  # Correctly display the fields
    list_filter = ['date']  # You can filter by booking date
    ordering = ['date']  # Order the list by booking date

admin.site.register(Booking, BookingAdmin)

