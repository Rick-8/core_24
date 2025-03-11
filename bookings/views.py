# bookings/views.py

from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking
from django.utils import timezone
from datetime import timedelta


# View for landing page (index)
def index(request):
    return render(request, 'index.html')


# View for booking page
def book_slot(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check if the booking limit for the day has been reached
            selected_date = form.cleaned_data['date']
            bookings_for_day = Booking.objects.filter(date=selected_date)
            if bookings_for_day.count() < 50:
                form.save()
                return redirect('confirmation', booking_id=form.instance.id)
            else:
                return render(request, 'bookings/full_day.html')
    else:
        form = BookingForm()

    return render(request, 'bookings/book_slot.html', {'form': form})


# Confirmation view
def confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'bookings/confirmation.html', {'booking': booking})
