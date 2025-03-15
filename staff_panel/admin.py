from django.contrib import admin
from .models import StaffDashboard


class StaffDashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(StaffDashboard, StaffDashboardAdmin)
