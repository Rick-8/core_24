from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bookings.views import home, custom_logout, logged_out  # Correct import from bookings app

urlpatterns = [
    path('', home, name='index'),  # Home view with the name 'index'
    path('admin/', admin.site.urls),
    path('logout/', custom_logout, name='custom_logout'),  # Custom logout view
    path('accounts/', include('allauth.urls')),  # Allauth URL configuration for authentication
    path('logged_out/', logged_out, name='logged_out'),  # Custom logged-out page after logout
    path('bookings/', include('bookings.urls')),  # Include URLs from the bookings app
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
