from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=False)
#     phone_number = forms.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format +919876543210 or 9876543210')])

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'phone_number')

# class CustomUserChangeForm(UserChangeForm):
#     email = forms.EmailField(required=False)
#     phone_number = forms.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format +919876543210 or 9876543210')])

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'password', 'role', 'phone_number')

# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=_('Phone number must be entered in the format: +919876543210 or 9876543210')
        )],
        widget=forms.TextInput(attrs={'placeholder': 'Optional'}),
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2', 'role', 'department', 'phone_number'
        )

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone:
            return None
        if CustomUser.objects.filter(phone_number=phone).exists():
            raise ValidationError(
                _("A user with this phone number already exists."),
                code='unique'
            )
        return phone

    # Add this for creation form (new users)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return None
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(
                _("A user with this email address already exists."),
                code='unique'
            )
        return email


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=_('Phone number must be entered in the format: +919876543210 or 9876543210')
        )],
        widget=forms.TextInput(attrs={'placeholder': 'Optional'}),
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'password', 'role', 'department', 'phone_number'
        )

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone:
            return None

        qs = CustomUser.objects.filter(phone_number=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                _("A user with this phone number already exists."),
                code='unique'
            )
        return phone

    # Add this — the key fix for edit form
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return None

        qs = CustomUser.objects.filter(email=email)
        if self.instance.pk:  # editing existing user → exclude self
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                _("A user with this email address already exists."),
                code='unique'
            )
        return email
