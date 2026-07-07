from random import randint

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.role = User.Role.CUSTOMER
        user.is_verified = True
        user.email_otp = str(randint(100000, 999999))
        if commit:
            user.save()
        return user


class VendorRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'business_name',
            'email',
            'phone_number',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.role = User.Role.VENDOR
        user.is_verified = True
        user.email_otp = str(randint(100000, 999999))
        if commit:
            user.save()
        return user
