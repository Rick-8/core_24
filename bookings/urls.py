from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('bookings/book-slot/', views.book_slot, name='book_slot'),
    path('bookings/booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('logged-out/', views.logged_out, name='logged_out'),
    path('logout/', views.custom_logout, name='logout'),
    path('join-up/', include('join_up.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
