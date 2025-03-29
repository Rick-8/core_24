from django.test import TestCase, Client
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from join_up.models import Customer
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404


class StaffDashboardJoinRequestTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpassword',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword',
            is_staff=False
        )
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
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpassword',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword',
            is_staff=False
        )
        self.staff_dashboard_url = reverse('staff_dashboard')
        self.delete_join_request_url = reverse(
            'staff_panel:delete_join_request', args=[1]
        )
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
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpassword',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword',
            is_staff=False
        )
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
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('staff_panel:user_admin'))


class ToggleUserActiveTests(TestCase):
    def setUp(self):
        """Set up test data including a staff user and a normal user."""
        self.staff_user = User.objects.create_user(
            username='staffuser', password='password123', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser', password='password123', is_active=True
        )
        self.client = Client()
        self.toggle_url = reverse(
            'staff_panel:toggle_user_active', args=[self.regular_user.id]
        )

    def test_toggle_user_active_as_staff(self):
        """Test that a staff user can toggle a user's active status."""
        self.client.login(username='staffuser', password='password123')

        response = self.client.post(self.toggle_url)
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active)
        self.assertRedirects(response, reverse('staff_panel:user_admin'))

        response = self.client.post(self.toggle_url)
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_active)


def test_toggle_user_active_redirects_if_not_logged_in(self):
    """
    Test that an unauthenticated user is redirected to the login page.
    """
    response = self.client.post(self.toggle_url)
    self.assertEqual(response.status_code, 302)

    login_url = settings.LOGIN_URL or reverse('admin:login')
    self.assertTrue(response.url.startswith(login_url))


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser, login_url='index')
def promote_to_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if not user.is_staff:
        user.is_staff = True
        user.save()
        messages.success(
            request, f'User {user.username} has been promoted to staff.'
        )
    else:
        messages.warning(
            request, f'User {user.username} is already a staff member.'
        )

    return redirect('staff_panel:user_admin')


class DeleteUserTest(TestCase):
    def setUp(self):
        """Set up a superuser and a regular user for testing."""
        self.superuser = User.objects.create_user(
            username='superuser',
            password='testpassword',
            is_superuser=True,
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword',
            is_superuser=False,
            is_staff=False
        )
        self.delete_user_url = reverse(
            'staff_panel:delete_user',
            args=[self.regular_user.id]
        )

    def test_delete_user_as_superuser(self):
        """Test that a superuser can delete a user successfully."""
        self.client.login(username='superuser', password='testpassword')

        self.assertTrue(User.objects.filter(id=self.regular_user.id).exists())

        response = self.client.post(self.delete_user_url)

        self.assertFalse(User.objects.filter(id=self.regular_user.id).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "User deleted successfully.")

        self.assertRedirects(response, reverse('staff_panel:user_admin'))

    def test_delete_user_without_login(self):
        """
        Test that an unauthenticated user is redirected to the login page.
        """
        response = self.client.post(self.delete_user_url)

        self.assertRedirects(response, settings.LOGIN_URL)


class UpdateUserSettingsTest(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='superuser',
            password='password',
            email='superuser@example.com'
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='password',
            email='regularuser@example.com'
        )
        self.regular_user.is_staff = False
        self.regular_user.save()

        self.update_user_url = reverse(
            'staff_panel:update_user_settings',
            args=[self.regular_user.id]
        )


def test_update_user_settings_as_superuser(self):
    self.client.login(username='superuser', password='password')

    self.client.post(self.update_user_url, {
        'username': 'updateduser',
        'email': 'updateduser@test.com',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False
    })
    self.regular_user.refresh_from_db()
    self.assertEqual(self.regular_user.username, 'updateduser')
    self.assertEqual(self.regular_user.email, 'updateduser@test.com')
    self.assertFalse(self.regular_user.is_staff)
    self.assertFalse(self.regular_user.is_superuser)

    self.regular_user.refresh_from_db()
    self.assertEqual(self.regular_user.username, 'updateduser')
    self.assertEqual(self.regular_user.email, 'updateduser@test.com')
    self.assertFalse(self.regular_user.is_staff)
    self.assertFalse(self.regular_user.is_superuser)

    self.assertFalse(self.regular_user.is_staff)


def test_update_user_settings_missing_fields(self):
    self.client.login(username='superuser', password='password')

    response = self.client.post(self.update_user_url, {
        'email': 'missingusername@test.com'
    })

    self.assertContains(response, "This field is required.", html=True)


class ResetPasswordTest(TestCase):

    def setUp(self):
        """
        Set up test environment by creating a superuser and a regular user
        for testing.
        Also, initializes the URL for resetting user password.
        """
        self.superuser = get_user_model().objects.create_superuser(
            username='superuser',
            password='password',
            email='superuser@example.com'
        )
        self.regular_user = get_user_model().objects.create_user(
            username='regularuser',
            password='password',
            email='regularuser@example.com'
        )
        self.reset_password_url = reverse(
            'staff_panel:reset_password',
            args=[self.regular_user.id]
        )

    def test_reset_password_as_superuser(self):
        """
        Test resetting the password as a superuser.
        The superuser should be able to reset the password for another user.
        """
        self.client.login(username='superuser', password='password')

        response = self.client.post(self.reset_password_url, {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })

        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password('newpassword123'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            f'Password reset successfully for {self.regular_user.username}'
        )

        self.assertRedirects(response, reverse('staff_panel:user_admin'))

    def test_get_reset_password_form(self):
        """
        Test accessing the password reset form via GET request.
        The form should be displayed correctly.
        """
        self.client.login(username='superuser', password='password')

        response = self.client.get(self.reset_password_url)
        self.assertContains(response, 'name="new_password1"')
        self.assertContains(response, 'name="new_password2"')
