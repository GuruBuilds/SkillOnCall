from django.db import models
from accounts.models import Customer, ServiceProvider, Service
from django.contrib.auth.models import User

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
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status_choices, max_length=10, default='Pending')
    description_of_problem = models.TextField()

    def __str__(self):
        return f"Booking {self.booking_id} by User {self.customer_id.user.username}"
