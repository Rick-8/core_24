from django.shortcuts import redirect
from django.urls import reverse


class StaffRequiredMiddleware:
    """
    Middleware to restrict access to staff-related pages.
    Only staff members and superusers can access any URL starting with 'staff_panel/'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith('/staff_panel/') and not request.user.is_staff:
            return redirect(reverse('index'))

        return self.get_response(request)
