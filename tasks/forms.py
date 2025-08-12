from django import forms
from .models import TaskModel

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['name', 'description', 'priority']

        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': '______________________________________________________________________________________________________________________________________________________________________________________________________________________________',
                'rows': 6,
                'class': 'underline'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': '____________________________________________________________',
                'rows': 6,
                'class': 'underline'
            }),
        }