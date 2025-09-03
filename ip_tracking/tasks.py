from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db import models

from ip_tracking.models import RequestLog, SuspiciousIP


@shared_task
def flag_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Find IPs exceeding 100 requests/hour
    heavy_hitters = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(count=models.Count("id"))
        .filter(count__gt=100)
    )

    for entry in heavy_hitters:
        ip = entry["ip_address"]
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason="Exceeded 100 requests in the last hour",
        )

    # Find IPs accessing sensitive paths
    sensitive_paths = ["/admin", "/login"]
    suspicious_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths,
    )

    for log in suspicious_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f"Accessed sensitive path {log.path}",
        )

    return "Suspicious IPs flagged"
