from django.contrib import admin
from .models import Booking, Profile
from .models import Profile


# Customizing the Booking admin display
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'membership_number', 'date', 'slot']  # Fields to display in the list
    list_filter = ['date', 'slot']  # Allow filtering by date and slot
    search_fields = ['user__username', 'email', 'membership_number']  # Allow searching by username, email, and membership number
    ordering = ['date']  # Order bookings by date


# Customizing the Profile admin display
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'membership_number', 'personal_address', 'phone_number_1', 'phone_number_2']  # Fields to display in the list
    search_fields = ['user__username', 'email', 'membership_number']  # Allow searching by username, email, and membership number


# Registering the models with customized admin views
admin.site.register(Booking, BookingAdmin)
admin.site.register(Profile, ProfileAdmin)
