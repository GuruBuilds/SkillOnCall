from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import (
    UserForm, CustomerForm, ServiceProviderForm, 
    PasswordForm, SignUpForm, WorkImageForm
)
from .models import Customer, ServiceProvider, Service, ServiceProviderImage
from home.views import index

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect(index)
            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please enter both username and password.")
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return edit_profile(request)
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)
        provider_form = ServiceProviderForm(request.POST)
        
        if form.is_valid() and customer_form.is_valid():
            user = form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            
            if customer.user_type == 'provider' and provider_form.is_valid():
                service_provider = provider_form.save(commit=False)
                service_provider.customer = customer
                service_provider.save()
                provider_form.save_m2m()  # For many-to-many relationships
            
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('index')
    else:
        form = SignUpForm()
        customer_form = CustomerForm()
        provider_form = ServiceProviderForm()
    
    return render(request, 'accounts/signup_view.html', {
        'form': form,
        'customer_form': customer_form,
        'provider_form': provider_form,
        'is_edit': False
    })

@login_required
def edit_profile(request):
    user = request.user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=user, user_type='customer')
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        customer_form = CustomerForm(request.POST, request.FILES, instance=customer)
        password_form = PasswordForm(request.POST)
        
        if user_form.is_valid() and customer_form.is_valid() and password_form.is_valid():
            user_form.save()
            customer_form.save()
            
            if password_form.cleaned_data['password']:
                user.set_password(password_form.cleaned_data['password'])
                user.save()
            
            if customer.user_type == 'provider':
                try:
                    provider = customer.serviceprovider
                    provider_form = ServiceProviderForm(request.POST, instance=provider)
                except ServiceProvider.DoesNotExist:
                    provider_form = ServiceProviderForm(request.POST)
                
                if provider_form.is_valid():
                    service_provider = provider_form.save(commit=False)
                    service_provider.customer = customer
                    service_provider.save()
                    provider_form.save_m2m()
            else:
                ServiceProvider.objects.filter(customer=customer).delete()
            
            messages.success(request, "Profile updated successfully!")
            return redirect('index')
    else:
        user_form = UserForm(instance=user)
        customer_form = CustomerForm(instance=customer)
        password_form = PasswordForm()
        
        try:
            provider = customer.serviceprovider
            provider_form = ServiceProviderForm(instance=provider)
        except ServiceProvider.DoesNotExist:
            provider_form = ServiceProviderForm()
    
    return render(request, 'accounts/signup_view.html', {
        'form': user_form,
        'customer_form': customer_form,
        'provider_form': provider_form,
        'password_form': password_form,
        'is_edit': True
    })

def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect(index)

@login_required
def upload_work_image(request):
    try:
        service_provider = request.user.customer.serviceprovider
    except ServiceProvider.DoesNotExist:
        messages.error(request, "You are not a service provider.")
        return redirect('index')
    
    if request.method == 'POST':
        form = WorkImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.service_provider = service_provider
            image.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect('upload_work_image')
    else:
        form = WorkImageForm()
    
    images = service_provider.images.all()
    return render(request, 'accounts/upload_work_image.html', {
        'form': form,
        'work_images': images
    })

@login_required
def delete_work_image(request, image_id):
    try:
        service_provider = request.user.customer.serviceprovider
        image = ServiceProviderImage.objects.get(id=image_id, service_provider=service_provider)
        image.delete()
        messages.success(request, "Image deleted successfully!")
    except (ServiceProvider.DoesNotExist, ServiceProviderImage.DoesNotExist):
        messages.error(request, "Image not found or you don't have permission.")
    return redirect('upload_work_image')