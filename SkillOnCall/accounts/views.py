from django.shortcuts import render, redirect
from .models import Customer, ServiceProvider, Service, ServiceProviderImage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,  logout
from django.contrib import messages
from home.views import index

# Create your views here.

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect(index)
            else:
                # Invalid login
                messages.error(request, "Invalid username or password.")

        else:
            messages.error(request, "Please enter both username and password.")
        return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        # Common fields
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        user_type = request.POST.get('user_type')

        # Edit profile case
        if request.user.is_authenticated:
            user = request.user
            customer = user.customer

            # Update user fields
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            if password:  # Only update password if provided
                user.set_password(password)
            user.save()

            # Update customer fields
            customer.phone_number = phone_number
            customer.address = address
            customer.city = city
            customer.user_type = user_type
            customer.save()

            # Handle service provider updates
            if user_type == 'provider':
                experience = request.POST.get('experience')
                description = request.POST.get('description')
                charge_per_hour = request.POST.get('charge_per_hour')
                services = request.POST.getlist('services_offered')

                service_provider, created = ServiceProvider.objects.get_or_create(
                    customer=customer,
                    defaults={
                        'experience': experience,
                        'description': description,
                        'charge_per_hour': charge_per_hour
                    }
                )

                if not created:
                    service_provider.experience = experience
                    service_provider.description = description
                    service_provider.charge_per_hour = charge_per_hour
                    service_provider.save()

                service_provider.services_offered.set(services)
            else:
                # Remove provider if downgraded to customer
                ServiceProvider.objects.filter(customer=customer).delete()

            messages.success(request, "Profile updated successfully!")
            return redirect('index')

        # Signup case
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            customer = Customer.objects.create(
                user=user,
                phone_number=phone_number,
                address=address,
                city=city,
                user_type=user_type
            )

            if user_type == 'provider':
                experience = request.POST.get('experience')
                description = request.POST.get('description')
                charge_per_hour = request.POST.get('charge_per_hour')
                services = request.POST.getlist('services_offered')

                service_provider = ServiceProvider.objects.create(
                    customer=customer,
                    experience=experience,
                    description=description,
                    charge_per_hour=charge_per_hour
                )
                service_provider.services_offered.set(services)

            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('index')

    # GET request - load form
    else:
        services = Service.objects.all()

        # If user is authenticated (edit profile case)
        if request.user.is_authenticated:
            user = request.user
            try:
                customer = user.customer
            except Customer.DoesNotExist:
                # Create a basic customer profile if it doesn't exist
                customer = Customer.objects.create(
                    user=user,
                    phone_number='',
                    address='',
                    city='',
                    user_type='customer'
                )

            # Prepare initial data
            initial_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': customer.phone_number,
                'address': customer.address,
                'city': customer.city,
                'user_type': customer.user_type,
            }

            try:
                provider = customer.serviceprovider
                initial_data.update({
                    'experience': provider.experience,
                    'description': provider.description,
                    'charge_per_hour': provider.charge_per_hour,
                    'services_offered': [s.id for s in provider.services_offered.all()],
                })
            except ServiceProvider.DoesNotExist:
                pass

            return render(request, 'accounts/signup_view.html', {
                'services': services,
                'initial_data': initial_data,
                'is_edit': True
            })

        # New signup form
        return render(request, 'accounts/signup_view.html', {
            'services': services,
            'initial_data': {},
            'is_edit': False
        })

def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect(index)

@login_required
def upload_work_image(request):
    try:
        # Check if the user is a service provider
        service_provider = request.user.customer.serviceprovider
    except ServiceProvider.DoesNotExist:
        messages.error(request, "You are not a service provider.")
        return redirect('index')
    if request.method == 'POST':
        image = request.FILES.get('image')
        description = request.POST.get('description')

        if image:
            ServiceProviderImage.objects.create(
                service_provider=service_provider,
                image=image,
                description=description
            )
            messages.success(request, "Image uploaded successfully!")
        else:
            messages.error(request, "Please provide image.")
        return redirect('upload_work_image')
    else:
        images = service_provider.images.all()
        return render(request, 'accounts/upload_work_image.html', {'work_images': images})

@login_required
def delete_work_image(request, image_id):
    try:
        # Check if the user is a service provider
        service_provider = request.user.customer.serviceprovider
    except ServiceProvider.DoesNotExist:
        messages.error(request, "You are not a service provider.")
        return redirect('index')

    try:
        image = ServiceProviderImage.objects.get(id=image_id, service_provider=service_provider)
        image.delete()
        messages.success(request, "Image deleted successfully!")
    except ServiceProviderImage.DoesNotExist:
        messages.error(request, "Image not found or you do not have permission to delete it.")
    return redirect('upload_work_image')