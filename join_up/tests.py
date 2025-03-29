from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Membership


class JoinUpViewTest(TestCase):
    """Test cases for the JoinUp view functionality."""

    def setUp(self):
        """Create a test user."""
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_join_up_view_post_valid(self):
        """Test the POST request to the JoinUp view with valid data."""
        self.client.login(username='testuser', password='testpassword')

        post_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone_number_1': '1234567890',
            'phone_number_2': ''
        }

        response = self.client.post(reverse('join_up:join_up'), data=post_data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Thank you for joining up! A member of staff will contact you within 24hrs."
        )

    def test_join_up_view_get(self):
        """Test the GET request to the JoinUp view."""
        response = self.client.get(reverse('join_up:join_up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'join_up/join_up.html')


class MembershipListViewTest(TestCase):
    """Test cases for the Membership list view."""

    def test_membership_list_view(self):
        """Test the GET request to view the list of memberships."""
        Membership.objects.create(name='Gold', price=100.0, active=True)
        Membership.objects.create(name='Silver', price=50.0, active=True)

        response = self.client.get(reverse('join_up:memberships'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gold')
        self.assertContains(response, 'Silver')


class EditMembershipViewTest(TestCase):
    """Test cases for the Edit Membership view."""

    def setUp(self):
        """Set up a superuser and a test membership."""
        self.superuser = get_user_model().objects.create_superuser(
            username='superuser', password='password'
        )
        self.membership = Membership.objects.create(
            name='Basic Membership',
            price=24.00,
            active=True
        )

    def test_edit_membership_post_valid_data(self):
        """Test the POST request to edit a membership with valid data."""
        self.client.login(username='superuser', password='password')

        response = self.client.post(reverse('join_up:edit_membership', args=[self.membership.id]), {
            'name': 'Updated Membership',
            'price': 30.00,
            'description': 'Updated description',
            'active': True
        })

        self.membership.refresh_from_db()
        self.assertEqual(self.membership.name, 'Updated Membership')
        self.assertEqual(self.membership.price, 30.00)

        self.assertRedirects(response, reverse('join_up:manage_memberships'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Membership updated successfully.')


class DeleteMembershipTestCase(TestCase):
    """Test cases for deleting a membership."""

    def setUp(self):
        """Create a superuser and membership."""
        self.superuser = get_user_model().objects.create_superuser(
            username="superuser", password="superpassword"
        )

        self.membership = Membership.objects.create(
            name="Premium Membership",
            price=29.99,
            description="Access to all gym facilities.",
            active=True
        )

        self.url = reverse('join_up:delete_membership', args=[self.membership.id])

    def test_delete_membership_success(self):
        """Test successful deletion of a membership."""
        self.client.login(username="superuser", password="superpassword")
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Membership.objects.filter(id=self.membership.id).count(), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Membership deleted successfully.")

    def test_delete_membership_invalid_method(self):
        """Test invalid method (GET instead of POST)."""
        self.client.login(username="superuser", password="superpassword")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Invalid request method.")


class MembershipCreateViewTest(TestCase):
    """Test cases for creating a new membership."""

    def setUp(self):
        """Set up a superuser."""
        self.superuser = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.client.login(username='admin', password='password123')
        self.url = reverse('join_up:create_membership')

    def test_create_membership_success(self):
        """Test successful membership creation."""
        data = {
            'name': 'Premium Membership',
            'price': 99.99,
            'description': 'Premium gym membership with all benefits.',
            'active': True
        }

        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('join_up:manage_memberships'))
        self.assertTrue(Membership.objects.filter(name='Premium Membership').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Membership created successfully.")

    def test_create_membership_invalid_data(self):
        """Test creation of a new membership with invalid data."""
        data = {
            'name': 'Invalid Membership',
            'price': 'invalid_price',
            'description': 'Invalid gym membership.',
            'active': True
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_create_membership_not_logged_in(self):
        """Test that an unauthenticated user is redirected to the login page."""
        self.client.logout()
        data = {
            'name': 'Another Membership',
            'price': 49.99,
            'description': 'Another membership type.',
            'active': True
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')