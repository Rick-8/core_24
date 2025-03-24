from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from datetime import date
from .models import Booking, Profile
from bookings.models import Profile
from django.core.exceptions import ValidationError


class TestCustomLogout(TestCase):
    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_logout_redirects(self):
        """Test that the user is logged out and redirected to the 'logged_out' page."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('custom_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('logged_out'))


class TestLoggedOut(TestCase):
    def test_logged_out_page(self):
        """Test that the 'logged_out' page renders correctly."""
        response = self.client.get(reverse('logged_out'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/logged_out.html')


class TestHomePage(TestCase):
    def test_home_page(self):
        """Test that the home page renders correctly."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class TestBookSlot(TestCase):
    def setUp(self):
        """Set up a user and some initial data for testing."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.booking_date = date.today()  # Ensure booking_date is set here

    def test_booking_slot_full(self):
        """Test that the booking fails when there are already 50 bookings for the slot."""
        # Simulate 50 existing bookings
        for _ in range(50):
            Booking.objects.create(user=self.user, date=self.booking_date)

        # The booking creation will raise a ValidationError if the limit is exceeded
        with self.assertRaises(ValidationError):
            Booking.objects.create(user=self.user, date=self.booking_date)

    def test_cancel_booking_success(self):
        """Test that a user can successfully cancel their booking."""
        # Create a booking
        booking = Booking.objects.create(user=self.user, date=date.today())
        # Attempt to cancel the booking
        response = self.client.post(reverse('book_slot'), {'cancel_booking': booking.id})

        # Check if the cancellation redirects correctly
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_slot'))

        # Ensure the booking is deleted
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

        # Check for success message
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Your booking has been successfully canceled.", messages)


class TestBookingConfirmation(TestCase):
    def setUp(self):
        """Set up a user and log them in for the booking confirmation."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

    def test_booking_confirmation(self):
        """Test that the booking confirmation page renders correctly."""
        # Simulate a booking confirmation view request
        response = self.client.get(reverse('booking_confirmation'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Ensure the correct template is used
        self.assertTemplateUsed(response, 'bookings/booking_confirmation.html')


class TestProfileView(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile, created = Profile.objects.get_or_create(
            user=self.user,
            defaults={"email": "test@example.com"}
        )


User = get_user_model()

class TestProfileView(TestCase):
    def setUp(self):
        """Set up a test user and profile."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Ensure the profile exists and avoid duplicate creation
        self.profile, created = Profile.objects.get_or_create(user=self.user)

    def test_profile_view_logged_in(self):
        """Test that the profile page renders correctly for a logged-in user."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('profile_view'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/profile.html')
        self.assertEqual(response.context['profile'], self.profile)

    def test_profile_view_redirect_if_not_logged_in(self):
        """Test that an unauthenticated user is redirected to login page."""
        response = self.client.get(reverse('profile_view'))
        self.assertRedirects(response, '/accounts/login/?next=/bookings/profile/')
