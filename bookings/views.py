# bookings/views.py
from django.shortcuts import render


def index(request):
    return render(request, 'bookings/index.html')  # Renders the home page of the bookings app


def book_slot(request):
    return render(request, 'book_slot.html')  # Renders the page to book a slot
