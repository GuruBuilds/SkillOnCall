from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, ServiceProvider, Service, ServiceProviderImage

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address', 'city', 'user_type', 'profile_image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs.update({
            'id': 'userTypeSelect',
            'onchange': 'toggleProviderFields()'
        })

class ServiceProviderForm(forms.ModelForm):
    services_offered = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': '3'}),
        required=False
    )
    
    class Meta:
        model = ServiceProvider
        fields = ['experience', 'description', 'charge_per_hour', 'services_offered']

class PasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        min_length=8,
        help_text="Leave blank to keep current password"
    )

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=Customer.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'id': 'userTypeSelect'})
    )
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

class WorkImageForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderImage
        fields = ['image', 'description']