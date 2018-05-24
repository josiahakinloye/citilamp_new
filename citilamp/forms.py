from django import forms

from .models import Contacts


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['full_name', 'email', 'message']
