from django import forms
from ..models.address import AddressModel
# from django.urls import reverse_lazy

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ['street', 'number', 'neighborhood', 'complement', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, Avenida, Travessa, etc...'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nº'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'complement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Casa, APT/ BL, etc...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PE, RJ, ...'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123-456-78'}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Brasil'}),
        }