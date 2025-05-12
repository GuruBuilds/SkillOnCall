from accounts.models import Customer, ServiceProvider

def service_provider_profile(request):
    if request.user.is_authenticated:
        try:
            cst = Customer.objects.get(user=request.user)
            try:
                service_provider = ServiceProvider.objects.get(customer=cst)
                return {'service_provider': service_provider}
            except ServiceProvider.DoesNotExist:
                pass
        except Customer.DoesNotExist:
            pass
    return {}
