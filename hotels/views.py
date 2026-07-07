from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BookingForm, HotelForm, HotelImageForm, HotelSearchForm
from .models import Booking, Hotel, HotelImage
from .services import attach_market_intelligence, vendor_analytics


def vendor_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")
        if not request.user.is_vendor:
            raise PermissionDenied('Vendor access required.')
        return view_func(request, *args, **kwargs)

    return wrapped


def hotel_list(request):
    form = HotelSearchForm(request.GET)
    hotels = Hotel.objects.filter(is_active=True).select_related('vendor').prefetch_related(
        Prefetch('images'),
        Prefetch('amenities'),
    )
    if form.is_valid():
        q = form.cleaned_data.get('q')
        location = form.cleaned_data.get('location')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        purpose = form.cleaned_data.get('purpose')
        sort = form.cleaned_data.get('sort')
        women_safe = form.cleaned_data.get('women_safe')
        emergency = form.cleaned_data.get('emergency')
        verified = form.cleaned_data.get('verified')
        if q:
            hotels = hotels.filter(
                Q(name__icontains=q)
                | Q(description__icontains=q)
                | Q(amenities__name__icontains=q)
            ).distinct()
        if location:
            hotels = hotels.filter(location__icontains=location)
        if min_price is not None:
            hotels = hotels.filter(offer_price__gte=min_price)
        if max_price is not None:
            hotels = hotels.filter(offer_price__lte=max_price)
        if women_safe or purpose == 'women_safe':
            hotels = hotels.filter(
                is_women_friendly=True,
                has_24x7_reception=True,
                has_cctv=True,
                has_verified_staff=True,
            )
        if emergency or purpose == 'emergency':
            hotels = hotels.filter(emergency_ready=True, has_24x7_reception=True, supports_late_checkin=True)
        if verified:
            hotels = hotels.filter(verified_photos=True)
        if sort == 'price_low':
            hotels = hotels.order_by('offer_price')
        elif sort == 'price_high':
            hotels = hotels.order_by('-offer_price')
        elif sort == 'rating':
            hotels = hotels.order_by('-rating')
        hotels = attach_market_intelligence(hotels, purpose)
        if sort == 'trust':
            hotels.sort(key=lambda hotel: hotel.trust_score, reverse=True)
        elif sort == 'safety':
            hotels.sort(key=lambda hotel: hotel.safety_score, reverse=True)
    else:
        hotels = attach_market_intelligence(hotels)
    return render(request, 'hotels/hotel_list.html', {'form': form, 'hotels': hotels})


def hotel_detail(request, slug):
    hotel = get_object_or_404(
        Hotel.objects.prefetch_related('images', 'amenities'),
        slug=slug,
        is_active=True,
    )
    hotel.market_fairness = attach_market_intelligence([hotel])[0].market_fairness
    form = BookingForm(request.POST or None)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")
        if not request.user.is_customer:
            messages.error(request, 'Vendor accounts cannot book hotels.')
            return redirect(hotel.get_absolute_url())
        if form.is_valid():
            booking = form.save(commit=False)
            booking.hotel = hotel
            booking.customer = request.user
            booking.total_price = hotel.offer_price * booking.nights
            try:
                booking.full_clean()
                booking.save()
            except Exception as exc:
                form.add_error(None, exc)
            else:
                messages.success(request, 'Booking confirmed. Payment is marked paid for this demo.')
                return redirect('my-bookings')
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'form': form})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('hotel')
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if request.method == 'POST':
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=['status'])
        messages.success(request, 'Booking cancelled.')
    return redirect('my-bookings')


@vendor_required
def vendor_dashboard(request):
    hotels = Hotel.objects.filter(vendor=request.user).prefetch_related('images', 'amenities')
    analytics = vendor_analytics(request.user)
    return render(request, 'hotels/vendor_dashboard.html', {'hotels': hotels, 'analytics': analytics})


@vendor_required
def hotel_create(request):
    form = HotelForm(request.POST or None)
    image_form = HotelImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        hotel = form.save(commit=False)
        hotel.vendor = request.user
        hotel.save()
        form.save_m2m()
        if request.FILES.get('image') and image_form.is_valid():
            image = image_form.save(commit=False)
            image.hotel = hotel
            image.save()
        messages.success(request, 'Hotel created.')
        return redirect('vendor-dashboard')
    return render(request, 'hotels/hotel_form.html', {'form': form, 'image_form': image_form, 'title': 'Add hotel'})


@vendor_required
def hotel_update(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug, vendor=request.user)
    form = HotelForm(request.POST or None, instance=hotel)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Hotel updated.')
        return redirect('vendor-dashboard')
    return render(request, 'hotels/hotel_form.html', {'form': form, 'title': 'Edit hotel', 'hotel': hotel})


@vendor_required
def hotel_delete(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug, vendor=request.user)
    if request.method == 'POST':
        hotel.delete()
        messages.success(request, 'Hotel deleted.')
        return redirect('vendor-dashboard')
    return render(request, 'hotels/confirm_delete.html', {'hotel': hotel})


@vendor_required
def hotel_images(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug, vendor=request.user)
    form = HotelImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        image = form.save(commit=False)
        image.hotel = hotel
        image.save()
        messages.success(request, 'Image uploaded.')
        return redirect('hotel-images', slug=hotel.slug)
    return render(request, 'hotels/hotel_images.html', {'hotel': hotel, 'form': form})


@vendor_required
def image_delete(request, pk):
    image = get_object_or_404(HotelImage, pk=pk, hotel__vendor=request.user)
    slug = image.hotel.slug
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted.')
    return redirect('hotel-images', slug=slug)


@vendor_required
def vendor_bookings(request):
    bookings = Booking.objects.filter(hotel__vendor=request.user).select_related('hotel', 'customer')
    return render(request, 'hotels/vendor_bookings.html', {'bookings': bookings})

# Create your views here.
