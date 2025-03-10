from django.contrib import admin
from .models import Booking
from django.core.exceptions import ValidationError
from django.utils.html import format_html

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'booking_status')  # Display user, date, and status
    list_filter = ('date',)  # Filter bookings by date
    search_fields = ('user__username',)  # Search by username
    ordering = ('-date',)  # Default ordering by date (descending)

    # Custom method to display booking status (whether it's valid or full)
    def booking_status(self, obj):
        # Check if the booking limit has been reached for the selected date
        bookings_count = Booking.objects.filter(date=obj.date).count()
        if bookings_count >= 100:
            return format_html('<span style="color: red;">Full</span>')
        return format_html('<span style="color: green;">Available</span>')
    booking_status.short_description = 'Booking Status'  # Column name in the admin panel

admin.site.register(Booking, BookingAdmin)
