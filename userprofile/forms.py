from account.forms import PasswordField
from account.models import EmailAddress
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class SignupForm(forms.Form):

    password = PasswordField(
        label=_("Password"),
        strip=settings.ACCOUNT_PASSWORD_STRIP,
    )
    password_confirm = PasswordField(
        label=_("Password (again)"),
        strip=settings.ACCOUNT_PASSWORD_STRIP,
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(), required=True)

    code = forms.CharField(
        max_length=64,
        required=False,
        widget=forms.HiddenInput()
    )

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data


class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    photo = forms.ImageField(required=False)


class FeedbackForm(forms.Form):
    message = forms.CharField(max_length=511, widget=forms.Textarea())
