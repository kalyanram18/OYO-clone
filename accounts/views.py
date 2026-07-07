from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CustomerRegistrationForm, EmailAuthenticationForm, VendorRegistrationForm
from .models import User


class RoleAwareLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_vendor:
            return reverse_lazy('vendor-dashboard')
        return reverse_lazy('hotel-list')


class AccountLogoutView(LogoutView):
    pass


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome. Your customer account is ready.')
            return redirect('hotel-list')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'account_type': 'Customer'})


def register_vendor(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Vendor account created. Add your first hotel to start receiving bookings.')
            return redirect('vendor-dashboard')
    else:
        form = VendorRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'account_type': 'Vendor'})


def login_with_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        otp = request.POST.get('otp', '').strip()
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            messages.error(request, 'No account exists with that email.')
        elif not otp:
            messages.info(request, f'Use OTP {user.email_otp or "123456"} for local demo login.')
            return render(request, 'accounts/login_otp.html', {'email': email, 'show_otp': True})
        elif otp == (user.email_otp or '123456'):
            login(request, user)
            return redirect('vendor-dashboard' if user.is_vendor else 'hotel-list')
        else:
            messages.error(request, 'The OTP did not match.')
            return render(request, 'accounts/login_otp.html', {'email': email, 'show_otp': True})
    return render(request, 'accounts/login_otp.html', {'show_otp': False})

# Create your views here.
