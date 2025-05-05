from django.shortcuts import render, get_object_or_404
from accounts.models import ServiceProvider, Service

# Create your views here.

def index(request):
    four_providers = ServiceProvider.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        four_providers = four_providers.exclude(customer=customer)[:4]
    else:
        four_providers = four_providers[:4]
    services = Service.objects.all()
    return render(request, 'index.html', {'four_providers': four_providers, 'services': services})

def all_providers(request):
    all_providers = ServiceProvider.objects.all()
    return render(request, 'all_providers.html', {'all_providers': all_providers})

def provider_detail(request, pk):
    provider = get_object_or_404(ServiceProvider, pk=pk)
    return render(request, 'provider_detail.html', {'provider': provider})

def explore_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    providers = ServiceProvider.objects.filter(services_offered=service)
    return render(request, 'explore_service.html', {'service': service, 'providers': providers})
