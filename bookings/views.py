from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Profile, ClosedDay
from .forms import ProfileForm, BookingForm
from datetime import date


def custom_logout(request):
    logout(request)
    return redirect('logged_out')


def logged_out(request):
    return render(request, 'account/logged_out.html')


def home(request):
    return render(request, "index.html")


@login_required
def book_slot(request):
    today = date.today()
    upcoming_bookings = Booking.objects.filter(user=request.user, date__gte=today)
    form = BookingForm(request.POST or None)

    if request.method == "POST":

        if "cancel_booking" in request.POST:
            booking_id = request.POST.get("cancel_booking")
            if booking_id:
                try:
                    booking = Booking.objects.get(id=booking_id)
                    if booking.user == request.user:
                        booking.delete()
                        messages.success(request, "Your booking has been successfully canceled.")
                    else:
                        messages.error(request, "You can only cancel your own bookings.")
                except Booking.DoesNotExist:
                    messages.error(request, "Booking not found.")
            return redirect("book_slot")

        if form.is_valid():
            booking_date = form.cleaned_data["date"]

            # Check if the gym is closed on the selected date
            if ClosedDay.objects.filter(date=booking_date).exists():
                messages.error(request, f"The gym is closed on {booking_date} due to maintenance.")
                return redirect("book_slot")

            # Check if the user has already booked for the date
            if Booking.objects.filter(date=booking_date, user=request.user).exists():
                messages.error(request, "You have already booked a session for this date.")
                return redirect("book_slot")

            # Check if the date has reached its booking limit
            if Booking.objects.filter(date=booking_date).count() >= 50:
                messages.error(request, "Sorry, all slots for this date are fully booked.")
                return redirect("book_slot")

            # Create and save the booking
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            messages.success(request, "Your session has been successfully booked!")
            return redirect("booking_confirmation")

    return render(request, "bookings/book_slot.html", {
        "form": form,
        "upcoming_bookings": upcoming_bookings
    })


def booking_confirmation(request):
    return render(request, "bookings/booking_confirmation.html")


@login_required
def profile_view(request):

    profile = Profile.objects.get(user=request.user)

    return render(request, 'bookings/profile.html', {'profile': profile})


@login_required
def delete_profile(request):
    """
    Allows the user to delete their profile. Optionally, deactivate the user account
    instead of deleting the user to retain data.
    """
    try:
        profile = Profile.objects.get(user=request.user)
        user = request.user
        profile.delete()

        user.is_active = False
        user.save()

        messages.success(request, "Your profile has been deleted successfully.")
        return redirect("logged_out")
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect("profile_view")


@login_required
def edit_profile(request):
    user = request.user  # Get the logged-in user

    # Check if the user already has a profile
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None  # If the profile does not exist, handle accordingly

    if request.method == 'POST':
        # Pass the logged-in user’s profile data into the form
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('profile_view')  # Redirect to the profile view page after saving
    else:
        form = ProfileForm(instance=profile)  # Initialize the form with the user's profile data

    return render(request, 'bookings/edit_profile.html', {'form': form})
