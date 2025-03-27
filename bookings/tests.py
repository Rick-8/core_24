from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from datetime import date
from .models import Booking, Profile
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string


class TestCustomLogout(TestCase):
    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_logout_redirects(self):
        """
        Test that the user is logged out and redirected
        to the 'logged_out' page.
        """
        self.client.login(username='testuser1', password='testpassword1')
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
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.booking_date = date.today()

    def test_booking_slot_full(self):
        """
        Test that the booking fails when there are already 50 bookings
        for the slot.
        """
        # Create 50 bookings for the same date
        for _ in range(50):
            Booking.objects.create(user=self.user, date=self.booking_date)

        # Try to create a new booking for the same date
        booking = Booking(user=self.user, date=self.booking_date)

        # Check if a ValidationError is raised due to the booking limit
        with self.assertRaises(ValidationError) as context:
            booking.full_clean()

        self.assertIn(
            "Booking limit reached for this date.",
            str(context.exception)
        )

    def test_cancel_booking(self):
        """Test that a user can successfully cancel their booking."""
        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            date=date.today()
        )

        # Simulate the user canceling the booking
        response = self.client.post(
            reverse('book_slot'), {'cancel_booking': booking.id}
        )

        # Check if the response is a redirect to the booking page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_slot'))

        # Ensure the booking was deleted
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

        # Check for success message
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Your booking has been successfully canceled.", messages)


class DeleteProfileTestCase(TestCase):
    def setUp(self):
        # Create a user with a unique username for each test
        username = (
            f"python-testuser-{get_random_string(8)}"
        )
        self.user = User.objects.create_user(
            username=username, password="testpassword"
        )

        self.profile, created = Profile.objects.get_or_create(user=self.user)

        self.client = Client()

    def test_delete_profile_success(self):

        self.client.login(username=self.user.username, password="testpassword")

        response = self.client.post(reverse('delete_profile'))

        self.assertEqual(
            response.status_code, 302
        )

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(
            Profile.objects.filter(user=self.user).count(), 0
        )
        new_user = User.objects.create_user(
            username="newuser", password="newpassword"
        )

        self.client.login(username="newuser", password="newpassword")

        response = self.client.post(reverse('delete_profile'))

        self.assertEqual(
            response.status_code, 302
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Profile not found.")
