from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from .models import Booking, Hotel
from .services import attach_market_intelligence


class BookingFlowTests(TestCase):
    def setUp(self):
        self.vendor = User.objects.create_user(
            username='vendor@example.com',
            email='vendor@example.com',
            password='Password123!',
            phone_number='9111111111',
            role=User.Role.VENDOR,
            is_verified=True,
        )
        self.customer = User.objects.create_user(
            username='customer@example.com',
            email='customer@example.com',
            password='Password123!',
            phone_number='9222222222',
            role=User.Role.CUSTOMER,
            is_verified=True,
        )
        self.hotel = Hotel.objects.create(
            vendor=self.vendor,
            name='Test Stay',
            description='A clean city hotel',
            location='Delhi',
            base_price=Decimal('3000.00'),
            offer_price=Decimal('2000.00'),
            verified_photos=True,
            response_time_minutes=20,
            completed_stays=50,
            has_24x7_reception=True,
            has_cctv=True,
            has_verified_staff=True,
            has_well_lit_area=True,
            workspace_ready=True,
        )

    def test_customer_can_book_hotel(self):
        self.client.force_login(self.customer)
        start = timezone.localdate() + timedelta(days=2)
        end = start + timedelta(days=3)

        response = self.client.post(
            reverse('hotel-detail', args=[self.hotel.slug]),
            {'start_date': start, 'end_date': end, 'guests': 2},
        )

        self.assertRedirects(response, reverse('my-bookings'))
        booking = Booking.objects.get()
        self.assertEqual(booking.total_price, Decimal('6000.00'))
        self.assertEqual(booking.nights, 3)

    def test_overlapping_booking_is_blocked(self):
        start = timezone.localdate() + timedelta(days=2)
        end = start + timedelta(days=2)
        Booking.objects.create(
            hotel=self.hotel,
            customer=self.customer,
            start_date=start,
            end_date=end,
            total_price=Decimal('4000.00'),
        )
        booking = Booking(
            hotel=self.hotel,
            customer=self.customer,
            start_date=start + timedelta(days=1),
            end_date=end + timedelta(days=1),
            total_price=Decimal('4000.00'),
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_vendor_cannot_book_hotel(self):
        self.client.force_login(self.vendor)
        start = timezone.localdate() + timedelta(days=2)
        end = start + timedelta(days=1)

        response = self.client.post(
            reverse('hotel-detail', args=[self.hotel.slug]),
            {'start_date': start, 'end_date': end, 'guests': 1},
        )

        self.assertRedirects(response, self.hotel.get_absolute_url())
        self.assertEqual(Booking.objects.count(), 0)

    def test_vendor_only_sees_own_hotels(self):
        other_vendor = User.objects.create_user(
            username='other@example.com',
            email='other@example.com',
            password='Password123!',
            phone_number='9333333333',
            role=User.Role.VENDOR,
        )
        Hotel.objects.create(
            vendor=other_vendor,
            name='Other Stay',
            description='Hidden from first vendor',
            location='Mumbai',
            base_price=Decimal('2500.00'),
            offer_price=Decimal('2100.00'),
        )
        self.client.force_login(self.vendor)

        response = self.client.get(reverse('vendor-dashboard'))

        self.assertContains(response, 'Test Stay')
        self.assertNotContains(response, 'Other Stay')

    def test_ai_work_matcher_prioritizes_workspace_hotels(self):
        leisure_hotel = Hotel.objects.create(
            vendor=self.vendor,
            name='Leisure Stay',
            description='A vacation hotel',
            location='Goa',
            base_price=Decimal('5000.00'),
            offer_price=Decimal('4500.00'),
            rating=Decimal('4.2'),
        )

        hotels = attach_market_intelligence(Hotel.objects.all(), purpose='work')

        self.assertEqual(hotels[0], self.hotel)
        self.assertGreater(self.hotel.trust_score, leisure_hotel.trust_score)

    def test_women_safe_filter_requires_safety_signals(self):
        safe_hotel = Hotel.objects.create(
            vendor=self.vendor,
            name='Safe Stay',
            description='Safety first hotel',
            location='Mumbai',
            base_price=Decimal('4200.00'),
            offer_price=Decimal('3000.00'),
            is_women_friendly=True,
            has_24x7_reception=True,
            has_cctv=True,
            has_verified_staff=True,
            has_well_lit_area=True,
        )
        self.client.get(reverse('hotel-list'), {'women_safe': 'on'})

        response = self.client.get(reverse('hotel-list'), {'women_safe': 'on'})

        self.assertContains(response, safe_hotel.name)
        self.assertNotContains(response, self.hotel.name)

# Create your tests here.
