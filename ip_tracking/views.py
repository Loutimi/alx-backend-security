from django.http import JsonResponse
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.views import View


class LoginView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Authenticated users → 10 requests/min
            decorator = ratelimit(key="user", rate=settings.RATELIMITS["authenticated"], block=True)
        else:
            # Anonymous users → 5 requests/min
            decorator = ratelimit(key="ip", rate=settings.RATELIMITS["anonymous"], block=True)

        wrapped_view = decorator(
            lambda req, *a, **kw: JsonResponse({"message": "Login attempt"})
        )
        return wrapped_view(request, *args, **kwargs)
