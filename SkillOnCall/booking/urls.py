from django.urls import path
from . import views

urlpatterns = [
    path('<int:provider_id>', views.book_service, name='book_service'),
    path('view-bookings/', views.view_bookings, name='view_bookings'),
    path('my-allocation/', views.my_allocation, name='my_allocation'),
    # path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    # path('<int:booking_id>/complete/', views.complete_booking, name='complete_booking'),
]
