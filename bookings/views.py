from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from datetime import date


# Custom logout view
def custom_logout(request):
    logout(request)  # Log out the user
    return redirect('logged_out')  # Redirect to logged_out page


# Logged out page view
def logged_out(request):
    return render(request, 'account/logged_out.html')  # Render the logged-out page


# Booking slot view (only accessible by logged-in users)
@login_required
def book_slot(request):
    today = date.today()
    upcoming_bookings = Booking.objects.filter(user=request.user, date__gte=today)
    form = BookingForm(request.POST or None)

    if request.method == "POST":
        # Handle booking cancellation
        if "cancel_booking" in request.POST:  # Handle cancellation request first
            booking_id = request.POST.get("cancel_booking")
            if booking_id:  # Make sure there's a valid booking ID
                print(f"Booking ID to delete: {booking_id}")  # Debugging print statement
                try:
                    booking = Booking.objects.get(id=booking_id)
                    if booking.user == request.user:
                        booking.delete()
                        messages.success(request, "Your booking has been successfully canceled.")
                    else:
                        messages.error(request, "You can only cancel your own bookings.")
                except Booking.DoesNotExist:
                    messages.error(request, "Booking not found.")
            else:
                messages.error(request, "No booking ID provided.")
            return redirect("book_slot")

        # Booking form submission logic...
        if form.is_valid():
            booking_date = form.cleaned_data["date"]

            # Check if the user already has a booking for this date
            existing_booking = Booking.objects.filter(date=booking_date, user=request.user).exists()
            if existing_booking:
                messages.error(request, "You have already booked a session for this date.")
                return redirect("book_slot")

            # Check if booking limit (50) is reached for the date
            if Booking.objects.filter(date=booking_date).count() >= 50:
                messages.error(request, "Sorry, all slots for this date are fully booked.")
                return redirect("book_slot")

            # Save the new booking
            booking = form.save(commit=False)
            booking.user = request.user  # Assign the logged-in user
            booking.save()

            messages.success(request, "Your session has been successfully booked!")
            return redirect("booking_confirmation")

    return render(request, "bookings/book_slot.html", {
        "form": form,
        "upcoming_bookings": upcoming_bookings
    })


# Confirmation after booking
def booking_confirmation(request):
    return render(request, "bookings/booking_confirmation.html")


# Home page view
def home(request):
    return render(request, 'index.html')
