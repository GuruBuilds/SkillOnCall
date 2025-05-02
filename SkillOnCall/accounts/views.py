from django.shortcuts import render
from .models import Customer, ServiceProvider, Service
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        user_type = request.POST.get('user_type')

        user = User.objects.create_user(username=username, password=password, email=email)
        customer = Customer.objects.create(user=user, phone_number=phone_number, address=address, city=city, user_type=user_type)

        if user_type == 'provider':
            experience = request.POST.get('experience')
            description = request.POST.get('description')
            charge_per_hour = request.POST.get('charge_per_hour')
            service_provider = ServiceProvider.objects.create(customer=customer, experience=experience, description=description, charge_per_hour=charge_per_hour)
            service_provider.services_offered.set(request.POST.getlist('services_offered'))

        login(request, user)
        return render(request, 'index.html')
        
    else:
        services = Service.objects.all()
        return render(request, 'accounts/signup_view.html', {'services': services})
    