import datetime
from django.utils.timezone import now
from .models import RequestLog

class RequestLoggingMiddleware:
    """
    Middleware that logs each incoming request's IP address,
    timestamp, and requested path into the database.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request before view is called
        self.log_request(request)

        # Continue to next middleware/view
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP address from request META."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]  # first in list
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip

    def log_request(self, request):
        """Save request details into RequestLog model."""
        ip = self.get_client_ip(request)
        path = request.path
        timestamp = now()

        # Save into DB
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            timestamp=timestamp
        )
