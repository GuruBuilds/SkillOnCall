from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from .models import Booking, Service, ServiceProvider
from booking.utils import send_booking_email


@login_required
def book_service(request, provider_id):
    customer = request.user.customer
    service_provider = get_object_or_404(ServiceProvider, id=provider_id)

    if request.method == 'POST':
        service_ids = request.POST.getlist('services')
        description_of_problem = request.POST.get('description_of_problem')
        services = Service.objects.filter(pk__in=service_ids)

        booking = Booking.objects.create(
            customer_id=customer,
            service_provider_id=service_provider,
            description_of_problem=description_of_problem
        )
        booking.service_id.set(services)

        # Email URLs
        base_url = request.build_absolute_uri('/')
        accept_url = urljoin(base_url, f"booking/accept-booking/{booking.access_token}/")
        decline_url = urljoin(base_url, f"booking/decline-booking/{booking.access_token}/")

        # Email Context
        context = {
            'provider_name': service_provider.customer.user.first_name,
            'customer_name': customer.user.first_name,
            'description_of_problem': description_of_problem,
            'services': services,
            'accept_url': accept_url,
            'decline_url': decline_url,
            'company_name': 'SkillOnCall',
            'current_year': now().year,
        }

        subject = "New Service Booking Request"
        success, error = send_booking_email(subject, service_provider.customer.user.email, 'email_templates/booking_notification.html', context)

        message = "Booking created successfully!"
        if not success:
            message += f" But email failed to send: {error}"

        bookings = Booking.objects.filter(customer_id=customer)
        return render(request, 'booking/all_bookings.html', {'message': message, 'bookings': bookings})

    return render(request, 'booking/book_service.html', {'provider': service_provider})

@login_required
def view_bookings(request):
    customer = request.user.customer
    bookings = Booking.objects.filter(customer_id=customer)
    return render(request, 'booking/all_bookings.html', {
        'bookings': bookings,
        'pending_bookings': bookings.filter(status='Pending'),
        'confirmed_bookings': bookings.filter(status='Confirmed'),
        'cancelled_bookings': bookings.filter(status='Cancelled'),
        'completed_bookings': bookings.filter(status='Completed'),
    })

@login_required
def my_allocation(request):
    provider = request.user.customer.serviceprovider
    bookings = Booking.objects.filter(service_provider_id=provider)
    return render(request, 'booking/my_allocation.html', {
        'bookings': bookings,
        'pending_bookings': bookings.filter(status='Pending'),
        'confirmed_bookings': bookings.filter(status='Confirmed'),
        'cancelled_bookings': bookings.filter(status='Cancelled'),
        'completed_bookings': bookings.filter(status='Completed'),
    })

@csrf_exempt
def accept_booking(request, access_token):
    booking = get_object_or_404(Booking.objects.select_related(
        'customer_id__user', 'service_provider_id__customer__user'
    ).prefetch_related('service_id'), access_token=access_token)

    if booking.status != 'Pending':
        return render(request, 'booking/thank_you.html', {
            'message': f'This booking has already been {booking.status.lower()}.'
        })

    booking.status = 'Confirmed'
    booking.save()

    context = {
        'status': 'Confirmed',
        'customer_name': booking.customer_id.user.first_name,
        'service_provider_name': booking.service_provider_id.customer.user.first_name,
        'description_of_problem': booking.description_of_problem,
        'services': booking.service_id.all(),
        'booking_date': booking.booking_date,
        'current_year': now().year,
    }

    subject = "Booking Confirmed"
    success, error = send_booking_email(subject, booking.customer_id.user.email, 'email_templates/booking_status_email.html', context)

    message = "Booking confirmed successfully!"
    if not success:
        message += f" But email failed: {error}"

    return render(request, 'booking/thank_you.html', {'message': message})

@csrf_exempt
def decline_booking(request, access_token):
    booking = get_object_or_404(Booking.objects.select_related(
        'customer_id__user', 'service_provider_id__customer__user'
    ), access_token=access_token)

    if booking.status != 'Pending':
        return render(request, 'booking/thank_you.html', {
            'message': f'This booking has already been {booking.status.lower()}.'
        })

    booking.status = 'Cancelled'
    booking.save()

    context = {
        'status': 'Declined',
        'customer_name': booking.customer_id.user.first_name,
        'service_provider_name': booking.service_provider_id.customer.user.first_name,
        'booking_date': booking.booking_date,
        'current_year': now().year,
    }

    subject = "Booking Declined"
    success, error = send_booking_email(subject, booking.customer_id.user.email, 'email_templates/booking_status_email.html', context)

    message = "Booking declined successfully!"
    if not success:
        message += f" But email failed: {error}"

    return render(request, 'booking/thank_you.html', {'message': message})
