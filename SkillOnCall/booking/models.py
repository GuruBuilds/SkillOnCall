from django.utils import timezone
import uuid
import base64

from django.db import models
from accounts.models import Customer, ServiceProvider, Service


# Create your models here.
class Booking(models.Model):
    status_choices = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    )
    booking_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_provider_id = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service_id = models.ManyToManyField(Service, related_name='services_booked')
    booking_date = models.DateTimeField(default=timezone.now())
    status = models.CharField(choices=status_choices, max_length=10, default='Pending')
    description_of_problem = models.TextField()
    access_token = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f"Booking {self.booking_id} by User {self.customer_id.user.username}"

    def save(self, *args, **kwargs):
        if not self.access_token:
            # Generate UUID and encode in URL-safe base64
            token = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=')
            self.access_token = token
        super().save(*args, **kwargs)
