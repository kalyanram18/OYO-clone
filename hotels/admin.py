from django.contrib import admin

from .models import Amenity, Booking, Hotel, HotelImage, HotelManager


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1


class HotelManagerInline(admin.TabularInline):
    model = HotelManager
    extra = 1


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'vendor',
        'location',
        'cover_image_url',
        'offer_price',
        'rating',
        'trust_score',
        'safety_score',
        'rooms_available',
        'is_active',
    )
    list_filter = (
        'is_active',
        'verified_photos',
        'is_women_friendly',
        'emergency_ready',
        'workspace_ready',
        'location',
        'rating',
    )
    search_fields = ('name', 'location', 'vendor__email')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('amenities',)
    inlines = [HotelImageInline, HotelManagerInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'customer', 'start_date', 'end_date', 'total_price', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'start_date')
    search_fields = ('hotel__name', 'customer__email')
    date_hierarchy = 'start_date'

# Register your models here.
