from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking, Service, ServiceProvider
from django.utils.timezone import now
from django.urls import reverse


@login_required
def book_service(request, provider_id):
    customer = request.user.customer
    service_provider = ServiceProvider.objects.get(id=provider_id)

    if request.method == 'POST':
        service_ids = request.POST.getlist('services')
        description_of_problem = request.POST.get('description_of_problem')

        services = Service.objects.filter(pk__in=service_ids)

        # Create the booking
        booking = Booking(
            customer_id=customer,
            service_provider_id=service_provider,
            description_of_problem=description_of_problem
        )
        booking.save()
        booking.service_id.set(services)

        # Prepare email content using the HTML template
        subject = "New Service Booking Request"
        base_url = request.build_absolute_uri('/')
        accept_decline_url = f"{base_url}accept-decline-booking/{booking.id}/"
        context = {
            'provider_name': service_provider,
            'customer_name': customer,
            'description_of_problem': description_of_problem,
            'services': services,
            'accept_decline_url': accept_decline_url, 
            'company_name': 'Your Company Name',
            'current_year': now().year,
        }

        html_message = render_to_string('email_templates/booking_notification.html', context)
        from_email = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, '', from_email, [service_provider.customer.user.email], html_message=html_message)
            message = "Booking created successfully and email sent to the provider!"
        except Exception as e:
            message = f"Booking created successfully, but there was an error sending the email: {str(e)}"

        bookings = Booking.objects.filter(customer_id=customer)

        return render(
            request,
            'booking/all_bookings.html',
            {'message': message, 'bookings': bookings}
        )

    elif request.method == 'GET':
        return render(request, 'booking/book_service.html', {'provider': service_provider})

@login_required
def view_bookings(request):
    customer = request.user.customer
    bookings = Booking.objects.filter(customer_id=customer)

    return render(request, 'booking/all_bookings.html', {'bookings': bookings})
