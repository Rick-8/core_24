from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm


# Custom logout view
def custom_logout(request):
    logout(request)  # Log out the user
    return redirect('logged_out')  # Redirect to logged_out page


# Logged out page view
def logged_out(request):
    return render(request, 'bookings/logged_out.html')  # Render the logged-out page


# Booking slot view (only accessible by logged-in users)
@login_required
def book_slot(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data["date"]

            # Check if user already has a booking for this date
            existing_booking = Booking.objects.filter(
                date=booking_date, name=request.user.get_full_name() or request.user.username).exists()

            if existing_booking:
                messages.error(request, "You have already booked a session for this date.")
                return redirect("book_slot")  # Reload the form with an error message

            # Check if booking limit (50) is reached
            if Booking.objects.filter(date=booking_date).count() >= 50:
                messages.error(request, "Sorry, all slots for this date are fully booked.")
                return redirect("book_slot")

            # Save new booking
            booking = form.save(commit=False)
            booking.name = request.user.get_full_name() or request.user.username
            booking.save()

            messages.success(request, "Your session has been successfully booked!")
            return redirect("booking_confirmation")
    else:
        form = BookingForm(initial={"name": request.user.get_full_name() or request.user.username})

    return render(request, "bookings/book_slot.html", {"form": form})


def booking_confirmation(request):
    return render(request, "bookings/booking_confirmation.html")


def home(request):
    return render(request, 'index.html')


def logged_out(request):
    return render(request, 'account/logged_out.html')
