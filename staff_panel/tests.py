from django.test import TestCase, Client
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from join_up.models import Customer
from staff_panel.forms import CustomUserCreationForm
from django.contrib.admin.views.decorators import staff_member_required


class StaffDashboardJoinRequestTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(username='staffuser', password='testpassword', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='testpassword', is_staff=False)
        self.staff_dashboard_url = reverse('staff_dashboard')

    def test_staff_dashboard_access_denied_for_non_staff(self):
        """Ensure non-staff users cannot access the staff dashboard."""
        self.client.login(username='regularuser', password='testpassword')
        response = self.client.get(self.staff_dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_staff_dashboard_access_granted_for_staff(self):
        """Ensure staff users can access the staff dashboard."""
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(self.staff_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff_panel/staff_dashboard.html')

    def test_staff_dashboard_redirects_anonymous_users(self):
        """Ensure unauthenticated users are redirected to the login page."""
        response = self.client.get(self.staff_dashboard_url)
        self.assertEqual(response.status_code, 302)


class StaffDashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(username='staffuser', password='testpassword', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='testpassword', is_staff=False)
        self.staff_dashboard_url = reverse('staff_dashboard')
        self.delete_join_request_url = reverse('staff_panel:delete_join_request', args=[1])
        self.customer = Customer.objects.create(id=1, name='Test Customer')

    def test_staff_dashboard_access_denied_for_non_staff(self):
        """Ensure non-staff users cannot access the staff dashboard."""
        self.client.login(username='regularuser', password='testpassword')
        response = self.client.get(self.staff_dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_staff_dashboard_access_granted_for_staff(self):
        """Ensure staff users can access the staff dashboard."""
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(self.staff_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff_panel/staff_dashboard.html')

    def test_staff_dashboard_redirects_anonymous_users(self):
        """Ensure unauthenticated users are redirected to the login page."""
        response = self.client.get(self.staff_dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_join_request_success_for_staff(self):
        """Ensure staff can successfully delete a join request."""
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.post(self.delete_join_request_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Customer.objects.filter(id=1).exists())


class CreateUserTest(TestCase):
    def setUp(self):
        """Create staff and non-staff users for testing."""
        self.client = Client()
        self.staff_user = User.objects.create_user(username='staffuser', password='testpassword', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='testpassword', is_staff=False)
        self.create_user_url = reverse('staff_panel:create_user')

    def test_create_user_access_for_staff(self):
        """Ensure only staff users can access the create user page."""
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(self.create_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff_panel/create_user.html')

    def test_create_user_post_valid_data(self):
        """Ensure a staff user can create a user successfully."""
        self.client.login(username='staffuser', password='testpassword')
        data = {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, 302)  # Redirects to user admin page
        self.assertTrue(User.objects.filter(username='newuser').exists())  # New user should be created
        self.assertRedirects(response, reverse('staff_panel:user_admin'))


class ToggleUserActiveTests(TestCase):
    def setUp(self):
        """Set up test data including a staff user and a normal user."""
        self.staff_user = User.objects.create_user(
            username='staffuser', password='password123', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser', password='password123'
        )
        self.client = Client()
        self.toggle_url = reverse('staff_panel:toggle_user_active', args=[self.regular_user.id])

    def test_toggle_user_active_as_staff(self):
        """Test that a staff user can toggle a user's active status."""
        self.client.login(username='staffuser', password='password123')
        response = self.client.post(self.toggle_url)

        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_active)
        self.assertRedirects(response, reverse('staff_panel:user_admin'))


        response = self.client.post(self.toggle_url)
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active)

    def test_toggle_user_active_redirects_if_not_logged_in(self):
        """Test that an unauthenticated user is redirected to the login page."""
        response = self.client.post(self.toggle_url)
        self.assertEqual(response.status_code, 302)
        login_url = reverse('admin:login')
        self.assertTrue(response.url.startswith(login_url))
