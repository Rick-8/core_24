# bookings/urls.py
from django.urls import path
from . import views  # Import the views to handle the routes

urlpatterns = [
    path('', views.index, name='index'),  # Default route for the bookings app (home page)
    path('book/', views.book_slot, name='book_slot'),
]
