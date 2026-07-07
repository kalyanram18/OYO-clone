from django import forms
from django.utils import timezone

from .models import Booking, Hotel, HotelImage


class HotelSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Hotel, amenity, purpose'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City or area'}))
    min_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Min Rs.'}))
    max_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max Rs.'}))
    purpose = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'AI stay matcher'),
            ('work', 'Work trip'),
            ('family', 'Family trip'),
            ('couple', 'Couple stay'),
            ('emergency', 'Emergency tonight'),
            ('women_safe', 'Women-safe stay'),
        ],
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Recommended'),
            ('price_low', 'Price low to high'),
            ('price_high', 'Price high to low'),
            ('rating', 'Top rated'),
            ('trust', 'Highest trust'),
            ('safety', 'Highest safety'),
        ],
    )
    women_safe = forms.BooleanField(required=False, label='Women-safe')
    emergency = forms.BooleanField(required=False, label='Emergency ready')
    verified = forms.BooleanField(required=False, label='Photo verified')


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'name',
            'description',
            'location',
            'address',
            'cover_image_url',
            'amenities',
            'base_price',
            'offer_price',
            'rating',
            'rooms_available',
            'verified_photos',
            'response_time_minutes',
            'completed_stays',
            'cancellation_count',
            'complaint_count',
            'is_women_friendly',
            'has_24x7_reception',
            'has_cctv',
            'has_verified_staff',
            'has_well_lit_area',
            'emergency_ready',
            'near_transport',
            'supports_late_checkin',
            'workspace_ready',
            'family_friendly',
            'couple_friendly',
            'local_experience_bundle',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.CheckboxSelectMultiple,
            'local_experience_bundle': forms.TextInput(attrs={'placeholder': 'Airport pickup + breakfast, city guide, coworking pass'}),
        }


class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ['image', 'caption']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'guests']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.localdate():
            raise forms.ValidationError('Check-in cannot be in the past.')
        return start_date
