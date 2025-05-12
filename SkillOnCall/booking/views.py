from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking, Service, ServiceProvider
from django.utils.timezone import now


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
        accept_decline_url = f"{base_url}accept-decline-booking/{booking.booking_id}/"
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
    pending_bookings = bookings.filter(status='Pending')
    confirmed_bookings = bookings.filter(status='Confirmed')
    cancelled_bookings = bookings.filter(status='Cancelled')
    completed_bookings = bookings.filter(status='Completed')

    return render(request, 'booking/all_bookings.html', {'bookings': bookings, 'pending_bookings': pending_bookings, 'confirmed_bookings': confirmed_bookings, 'cancelled_bookings': cancelled_bookings, 'completed_bookings': completed_bookings})

@login_required
def my_allocation(request):
    provider = request.user.customer.serviceprovider
    bookings = Booking.objects.filter(service_provider_id=provider)
    pending_bookings = bookings.filter(status='Pending')
    confirmed_bookings = bookings.filter(status='Confirmed')
    cancelled_bookings = bookings.filter(status='Cancelled')
    completed_bookings = bookings.filter(status='Completed')

    return render(request, 'booking/my_allocation.html', {'bookings': bookings, 'pending_bookings': pending_bookings, 'confirmed_bookings': confirmed_bookings, 'cancelled_bookings': cancelled_bookings, 'completed_bookings': completed_bookings})

@login_required
def confirm_booking(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    booking.status = 'Confirmed'
    booking.save()

    # TODO for Gurupreet: send email to customer after confirmation
    # Send confirmation email to the customer
    # subject = "Booking Confirmation"
    # context = {
    #     'customer_name': booking.customer_id.user.first_name,
    #     'service_provider_name': booking.service_provider_id.customer.user.first_name,
    #     'description_of_problem': booking.description_of_problem,
    #     'services': booking.service_id.all(),
    #     'company_name': 'Your Company Name',
    #     'current_year': now().year,
    # }
    # html_message = render_to_string('email_templates/booking_confirmation.html', context)
    # from_email = settings.EMAIL_HOST_USER

    # try:
    #     send_mail(subject, '', from_email, [booking.customer_id.user.email], html_message=html_message)
    # except Exception as e:
    #     print(f"Error sending confirmation email: {str(e)}")

    return redirect('my_allocation')

@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    booking.status = 'Cancelled'
    booking.save()

    # TODO for Gurupreet: send email to customer after cancellation

    return redirect('my_allocation')