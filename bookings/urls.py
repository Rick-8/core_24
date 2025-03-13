from django.urls import path
from . import views  # Import the views to handle the routes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='index'),  # This will route the root URL to your home view
    path("book-slot/", views.book_slot, name="book_slot"),
    path("booking-confirmation/", views.booking_confirmation, name="booking_confirmation"),
    path("logout/", views.custom_logout, name="custom_logout"),
    path("logged-out/", views.logged_out, name="logged_out"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
