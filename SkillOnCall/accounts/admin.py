from django.contrib import admin
from .models import Customer, ServiceProvider, Service, ServiceProviderImage


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'city', 'user_type')
    search_fields = ('user__username', 'phone_number', 'city')
    list_filter = ('user_type',)
    ordering = ('user',)
admin.site.register(Customer, CustomerAdmin)


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'experience', 'description', 'charge_per_hour')
    search_fields = ('customer__user__username', 'description')
    list_filter = ('experience',)
    ordering = ('customer',)
admin.site.register(ServiceProvider, ServiceProviderAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
admin.site.register(Service, ServiceAdmin)

class ServiceProviderImageAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'image', 'description')
    search_fields = ('service_provider__customer__user__username', 'description')
    ordering = ('service_provider',)
admin.site.register(ServiceProviderImage, ServiceProviderImageAdmin)