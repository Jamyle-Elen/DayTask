from django import forms
from .models import UserModel

class UserModel(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email', 'passoword']