from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import RequestLog, BlockedIP

class RequestLoggingMiddleware:
    """
    Middleware that logs requests and blocks IPs listed in BlockedIP.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)

        # Block IP if in BlockedIP table
        if BlockedIP.objects.filter(ip_address=client_ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Otherwise, log the request
        self.log_request(request, client_ip)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address from request META."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip

    def log_request(self, request, client_ip):
        """Save request details into RequestLog model."""
        RequestLog.objects.create(
            ip_address=client_ip,
            path=request.path,
            timestamp=now()
        )
