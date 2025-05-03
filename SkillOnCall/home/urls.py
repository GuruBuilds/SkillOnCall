from django.urls import path
from .views import index, all_providers, provider_detail

urlpatterns = [
    path('', index, name='index'),
    path('providers/', all_providers, name='all_providers'),
    path('provider/<int:pk>/', provider_detail, name='provider_detail'),

]
