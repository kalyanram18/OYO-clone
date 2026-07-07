from django.urls import path

from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel-list'),
    path('hotels/<slug:slug>/', views.hotel_detail, name='hotel-detail'),
    path('bookings/', views.my_bookings, name='my-bookings'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel-booking'),
    path('vendor/', views.vendor_dashboard, name='vendor-dashboard'),
    path('vendor/hotels/add/', views.hotel_create, name='hotel-create'),
    path('vendor/hotels/<slug:slug>/edit/', views.hotel_update, name='hotel-update'),
    path('vendor/hotels/<slug:slug>/delete/', views.hotel_delete, name='hotel-delete'),
    path('vendor/hotels/<slug:slug>/images/', views.hotel_images, name='hotel-images'),
    path('vendor/images/<int:pk>/delete/', views.image_delete, name='image-delete'),
    path('vendor/bookings/', views.vendor_bookings, name='vendor-bookings'),
]
