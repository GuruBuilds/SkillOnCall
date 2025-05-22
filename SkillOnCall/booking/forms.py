from django import forms
from .models import Booking, Service

class BookingEditForm(forms.ModelForm):
    service_id = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=True,
        label='Services'
    )
    booking_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=False,
        label='Booking Date'
    )

    class Meta:
        model = Booking
        fields = ['service_id', 'description_of_problem', 'booking_date']
        widgets = {
            'description_of_problem': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
