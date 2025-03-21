from django.contrib import admin
from .models import Booking, Profile, ClosedDay


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'closed_for_maintenance')
    list_filter = ('closed_for_maintenance',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'email', 'membership_number', 'personal_address',
        'phone_number_1', 'phone_number_2'
    ]
    search_fields = ['user__username', 'email', 'membership_number']


class ClosedDayAdmin(admin.ModelAdmin):
    list_display = ['date', 'reason']
    search_fields = ['date', 'reason']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ClosedDay, ClosedDayAdmin)
