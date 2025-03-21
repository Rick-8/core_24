from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Profile, ClosedDay
from .forms import ProfileForm, BookingForm
from datetime import date


def custom_logout(request):
    """
    Logs the user out and redirects to the 'logged_out' page.
    """
    logout(request)
    return redirect('logged_out')


def logged_out(request):
    """
    Renders the logged-out confirmation page after user logout.
    """
    return render(request, 'account/logged_out.html')


def home(request):
    """
    Renders the main landing page for the gym website.
    """
    return render(request, "index.html")


@login_required
def book_slot(request):
    """
    Allows the user to book a gym slot. It checks for existing bookings,
    gym closure, and availability before confirming the booking.
    """
    today = date.today()
    upcoming_bookings = Booking.objects.filter(
        user=request.user, date__gte=today
    )
    form = BookingForm(request.POST or None)

    if request.method == "POST":
        if "cancel_booking" in request.POST:
            booking_id = request.POST.get("cancel_booking")
            if booking_id:
                try:
                    booking = Booking.objects.get(id=booking_id)
                    if booking.user == request.user:
                        booking.delete()
                        messages.success(
                            request,
                            "Your booking has been successfully canceled."
                        )
                    else:
                        messages.error(
                            request, "You can only cancel your own bookings."
                        )
                except Booking.DoesNotExist:
                    messages.error(request, "Booking not found.")
            return redirect("book_slot")

        if form.is_valid():
            booking_date = form.cleaned_data["date"]

            if ClosedDay.objects.filter(date=booking_date).exists():
                messages.error(
                    request,
                    f"The gym is closed on {booking_date} due to maintenance."
                )
                return redirect("book_slot")

        if Booking.objects.filter(
                date=booking_date, user=request.user).exists():
            messages.error(
                request, "You have already booked a session for this date."
            )
            return redirect("book_slot")

        if Booking.objects.filter(date=booking_date).count() >= 50:
            messages.error(
                request, "Sorry, all slots for this date are fully booked."
            )
            return redirect("book_slot")

        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()

        messages.success(
            request, "Your session has been successfully booked!")
        return redirect("booking_confirmation")

    return render(
        request, "bookings/book_slot.html",
        {"form": form, "upcoming_bookings": upcoming_bookings}
    )


def booking_confirmation(request):
    """
    Renders the booking confirmation page after a successful booking.
    """
    return render(request, "bookings/booking_confirmation.html")


@login_required
def profile_view(request):
    """
    Displays the user's profile information.
    """
    profile = Profile.objects.get(user=request.user)

    return render(request, 'bookings/profile.html', {'profile': profile})


@login_required
def delete_profile(request):
    """
    Allows the user to delete their profile. Optionally, deactivate the user
    account instead of deleting to retain data.
    """
    try:
        profile = Profile.objects.get(user=request.user)
        user = request.user
        profile.delete()

        user.is_active = False
        user.save()

        messages.success(
            request, "Your profile has been deleted successfully.")
        return redirect("logged_out")
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect("profile_view")


@login_required
def edit_profile(request):
    """
    Allows the user to edit their profile details.
    """
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'bookings/edit_profile.html', {'form': form})
