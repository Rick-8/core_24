from django.contrib import admin
from .models import Booking, Profile


# Customizing the Booking admin display
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']  # Only fields that exist in the Booking model
    list_filter = ['date']  # You can filter by the 'date' field


# Customizing the Profile admin display
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'membership_number', 'personal_address', 'phone_number_1', 'phone_number_2']  # Fields to display in the list
    search_fields = ['user__username', 'email', 'membership_number']  # Allow searching by username, email, and membership number


# Registering the models with customized admin views
admin.site.register(Booking, BookingAdmin)
admin.site.register(Profile, ProfileAdmin)
