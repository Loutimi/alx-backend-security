from django.db import models

class RequestLog(models.Model):
    """
    Model to log IP addresses, timestamp and path of
    every incoming request.
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.ip_address} - {self.path} @ {self.timestamp}"


class BlockedIP(models.Model):
    """
    Model to store blocked IP addresses.
    """
    ip_address = models.GenericIPAddressField(unique=True)
