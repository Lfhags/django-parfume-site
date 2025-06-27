from django import forms
from . models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control border-brown rounded-4 mb-2'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control border-brown rounded-4 mb-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-brown rounded-4 mb-2'}),
            'address': forms.TextInput(attrs={'class': 'form-control border-brown rounded-4 mb-2'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control border-brown rounded-4 mb-2'}),
            'city': forms.TextInput(attrs={'class': 'form-control border-brown rounded-4 mb-2'}),
        }
        