from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('host_name', 'port')
        widgets = {
            'host_name': forms.TextInput(attrs={'placeholder': 'Please input host name.'}),
            'port': forms.NumberInput(attrs={'placeholder': 'Please input port number.', 'min': 1}),
        }
