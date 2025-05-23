from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    user_type = models.CharField(choices=[('customer', 'Customer'), ('provider', 'Service Provider')], default='customer')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class ServiceProvider(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    experience = models.IntegerField()
    description = models.TextField()
    charge_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    services_offered = models.ManyToManyField('Service', name='services_offered')

    def __str__(self):
        return self.customer.user.username

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ServiceProviderImage(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='service_provider_images/')
    description = models.TextField()

    def __str__(self):
        return f"Image for {self.service_provider.customer.user.username}"
