from django.shortcuts import render
from accounts.models import Customer, ServiceProvider, Service
from booking.models import Booking
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def book_service(request, provider_id):
    customer = request.user.customer
    service_provider = ServiceProvider.objects.get(id=provider_id)

    if request.method == 'POST':
        service_ids = request.POST.getlist('services')
        description_of_problem = request.POST.get('description_of_problem')

        services = Service.objects.filter(pk__in=service_ids)

        booking = Booking(
            customer_id=customer,
            service_provider_id=service_provider,
            description_of_problem=description_of_problem
        )
        booking.save()
        booking.service_id.set(services)

        message = "Booking created successfully!"
        bookings = Booking.objects.filter(customer_id=customer)

        return render(
            request,
            'booking/all_bookings.html',
            {'message': message, 'bookings': bookings}
        )

    if request.method == 'GET':
        return render(request, 'booking/book_service.html', {'provider': service_provider})

@login_required
def view_bookings(request):
    customer = request.user.customer
    bookings = Booking.objects.filter(customer_id=customer)

    return render(request, 'booking/all_bookings.html', {'bookings': bookings})
