from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class LoginForm(forms.Form):
    """Simple login form with no password."""

    email = forms.EmailField(
        label=_('Your email address'),
        required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})


class RegisterForm(forms.ModelForm):
    """Form used to create new user accounts."""

    email = forms.EmailField(
        label=_('Your email address'),
        required=True,
        help_text=_('We will send a confirmation link to '
                    'this address before creating the account.'))
    full_name = forms.CharField(
        label=_('Your full name'),
        required=True,
        help_text=_('This is how we will address you in our communications.'))

    class Meta:
        model = User
        fields = ['full_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'autofocus': True})
