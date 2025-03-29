from django.contrib.messages.middleware import MessageMiddleware
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class StaffRequiredMiddleware:
    """
    Middleware to restrict access to staff-related pages.
    Only staff members and superusers can access any URL
    starting with 'staff_panel/'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/staff_panel/') and not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        if request.path.startswith('/staff_panel/') and not request.user.is_staff:
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)


class CustomMessageMiddleware(MessageMiddleware):
    def process_response(self, request, response):
        if hasattr(request, 'user') and request.user.is_authenticated:
            messages.get_messages(request)

        return super().process_response(request, response)
