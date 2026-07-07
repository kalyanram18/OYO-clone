from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.RoleAwareLoginView.as_view(), name='login'),
    path('logout/', views.AccountLogoutView.as_view(), name='logout'),
    path('register/', views.register_customer, name='register'),
    path('vendor/register/', views.register_vendor, name='vendor-register'),
    path('login/otp/', views.login_with_otp, name='login-otp'),
]
