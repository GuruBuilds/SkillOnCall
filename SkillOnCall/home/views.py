from django.shortcuts import render, get_object_or_404
from accounts.models import ServiceProvider

# Create your views here.

def index(request):
    four_providers = ServiceProvider.objects.all()[:4]
    return render(request, 'index.html', {'four_providers': four_providers})

def all_providers(request):
    all_providers = ServiceProvider.objects.all()
    return render(request, 'all_providers.html', {'all_providers': all_providers})

def provider_detail(request, pk):
    provider = get_object_or_404(ServiceProvider, pk=pk)
    return render(request, 'provider_detail.html', {'provider': provider})
