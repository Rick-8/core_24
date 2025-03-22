from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import date
from bookings.models import Booking, ClosedDay
from bookings.forms import BookingForm
from unittest.mock import patch


class ViewsTestCase(TestCase):

    def setUp(self):
        """
        Set up a test user for testing purposes.
        """
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_custom_logout_redirects(self):
        """
        Test if the user is logged out and redirected to 'logged_out' page.
        """
        response = self.client.get(reverse('custom_logout'))
        # Test if the user is redirected to the 'logged_out' page
        self.assertRedirects(response, reverse('logged_out'))

        # Test if the session is cleared after logout
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_logged_out_page(self):
        """
        Test if the 'logged_out' page renders correctly after logout.
        """
        # Log out the user
        self.client.logout()

        # Access the 'logged_out' page
        response = self.client.get(reverse('logged_out'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/logged_out.html')

    def test_home_page(self):
        """
        Test if the home page loads correctly.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class BookSlotViewTest(TestCase):

    def setUp(self):
        """
        Set up a test user for testing purposes and create a gym slot for booking.
        """
        self.client = self.client_class()
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_book_slot_view_accessible(self):
        """
        Test if the book slot page is accessible and requires login.
        """
        response = self.client.get(reverse('book_slot'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/book_slot.html')

    @patch('bookings.views.BookingForm')
    def test_booking_for_available_slot(self, MockBookingForm):
        """
        Test booking a slot if all conditions are met.
        """
        form_mock = MockBookingForm.return_value
        form_mock.is_valid.return_value = True
        form_mock.cleaned_data = {'date': date.today()}
        response = self.client.post(reverse('book_slot'), {'date': date.today()})

        self.assertRedirects(response, reverse('booking_confirmation'))
        self.assertEqual(len(messages.get_messages(response.wsgi_request)), 1)

    def test_cancel_booking(self):
        """
        Test if a user can cancel a booking.
        """
        booking = Booking.objects.create(user=self.user, date=date.today())
        response = self.client.post(reverse('book_slot'), {'cancel_booking': booking.id})

        self.assertEqual(Booking.objects.count(), 0)
        self.assertRedirects(response, reverse('book_slot'))
        self.assertTrue(
            any(msg.message == 'Your booking has been successfully canceled.' for msg in messages.get_messages(response.wsgi_request))
        )

    def test_cancel_booking_error_not_owner(self):
        """
        Test if a user tries to cancel a booking they don't own.
        """
        other_user = get_user_model().objects.create_user(username='otheruser', password='testpassword')
        booking = Booking.objects.create(user=other_user, date=date.today())

        response = self.client.post(reverse('book_slot'), {'cancel_booking': booking.id})

        self.assertEqual(Booking.objects.count(), 1)
        self.assertRedirects(response, reverse('book_slot'))
        self.assertTrue(
            any(msg.message == 'You can only cancel your own bookings.' for msg in messages.get_messages(response.wsgi_request))
        )

    def test_booking_gym_closed(self):
        """
        Test if the gym is closed on a given date.
        """
        ClosedDay.objects.create(date=date.today())
        response = self.client.post(reverse('book_slot'), {'date': date.today()})

        self.assertRedirects(response, reverse('book_slot'))
        self.assertTrue(
            any(msg.message == f"The gym is closed on {date.today()} due to maintenance." for msg in messages.get_messages(response.wsgi_request))
        )

    def test_booking_already_exists(self):
        """
        Test if the user tries to book the same day twice.
        """
        Booking.objects.create(user=self.user, date=date.today())
        response = self.client.post(reverse('book_slot'), {'date': date.today()})

        self.assertRedirects(response, reverse('book_slot'))
        self.assertTrue(
            any(msg.message == 'You have already booked a session for this date.' for msg in messages.get_messages(response.wsgi_request))
        )

    def test_booking_slots_full(self):
        """
        Test if the slots for a specific day are fully booked.
        """
        for _ in range(50):
            Booking.objects.create(user=self.user, date=date.today())

        self.client.login(username='testuser', password='12345')

        response = self.client.post(reverse('book_slot'), {'date': date.today()})

        self.assertRedirects(response, reverse('book_slot'))

        self.assertTrue(
            any(msg.message == 'Sorry, all slots for this date are fully booked.' for msg in messages.get_messages(response.wsgi_request))
        )
