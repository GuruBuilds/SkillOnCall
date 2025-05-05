from django.contrib import admin

# Register your models here.
from .models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'customer_id', 'service_provider_id', 'booking_date', 'status')
    list_filter = ('status',)
    search_fields = ('customer_id__user__username', 'service_provider_id__user__username')
    ordering = ('-booking_date',)
    date_hierarchy = 'booking_date'
    list_per_page = 10
    list_editable = ('status',)
    actions = ['mark_as_confirmed', 'mark_as_cancelled']
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='Confirmed')
        self.message_user(request, "Selected bookings marked as confirmed.")
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
        self.message_user(request, "Selected bookings marked as cancelled.")
    mark_as_cancelled.short_description = "Mark selected bookings as cancelled"