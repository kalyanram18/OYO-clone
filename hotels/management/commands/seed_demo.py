from decimal import Decimal

from django.core.management.base import BaseCommand

from accounts.models import User
from hotels.models import Amenity, Hotel, HotelManager


class Command(BaseCommand):
    help = 'Create demo users, amenities, and hotels.'

    def handle(self, *args, **options):
        amenities = {}
        for name in ['WiFi', 'Breakfast', 'Pool', 'Parking', 'Air conditioning', 'Workspace']:
            amenities[name], _ = Amenity.objects.get_or_create(name=name)

        vendor, created = User.objects.get_or_create(
            email='vendor@example.com',
            defaults={
                'username': 'vendor@example.com',
                'first_name': 'Demo',
                'last_name': 'Vendor',
                'phone_number': '9000000001',
                'business_name': 'Metro Stays',
                'role': User.Role.VENDOR,
                'is_verified': True,
            },
        )
        if created:
            vendor.set_password('Password123!')
            vendor.save()

        customer, created = User.objects.get_or_create(
            email='customer@example.com',
            defaults={
                'username': 'customer@example.com',
                'first_name': 'Demo',
                'last_name': 'Customer',
                'phone_number': '9000000002',
                'role': User.Role.CUSTOMER,
                'is_verified': True,
            },
        )
        if created:
            customer.set_password('Password123!')
            customer.save()

        hotel_specs = [
            {
                'name': 'OYO Townhouse Central Park',
                'location': 'Delhi',
                'base_price': Decimal('3600.00'),
                'offer_price': Decimal('2499.00'),
                'description': 'Modern business hotel near metro access.',
                'cover_image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.5'),
                'verified_photos': True,
                'response_time_minutes': 18,
                'completed_stays': 148,
                'cancellation_count': 2,
                'complaint_count': 1,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'emergency_ready': True,
                'near_transport': True,
                'supports_late_checkin': True,
                'workspace_ready': True,
                'family_friendly': True,
                'local_experience_bundle': 'Airport pickup + breakfast',
            },
            {
                'name': 'OYO Flagship Marine Drive',
                'location': 'Mumbai',
                'base_price': Decimal('5200.00'),
                'offer_price': Decimal('3799.00'),
                'description': 'Sea-facing stay with quick access to offices and cafes.',
                'cover_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.6'),
                'verified_photos': True,
                'response_time_minutes': 25,
                'completed_stays': 212,
                'cancellation_count': 1,
                'complaint_count': 1,
                'is_women_friendly': True,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'emergency_ready': True,
                'near_transport': True,
                'supports_late_checkin': True,
                'couple_friendly': True,
                'family_friendly': True,
                'local_experience_bundle': 'Late checkout + local food walk',
            },
            {
                'name': 'OYO Rooms Garden District',
                'location': 'Bengaluru',
                'base_price': Decimal('4100.00'),
                'offer_price': Decimal('2899.00'),
                'description': 'Quiet rooms, fast WiFi, and breakfast for work trips.',
                'cover_image_url': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.4'),
                'verified_photos': True,
                'response_time_minutes': 15,
                'completed_stays': 96,
                'cancellation_count': 0,
                'complaint_count': 0,
                'is_women_friendly': True,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'near_transport': True,
                'workspace_ready': True,
                'local_experience_bundle': 'Coworking day pass',
            },
            {
                'name': 'OYO Elite Residency Hitech City',
                'location': 'Hyderabad',
                'base_price': Decimal('4400.00'),
                'offer_price': Decimal('3199.00'),
                'description': 'Tech-corridor stay with meeting-friendly rooms, breakfast, and quick cab access.',
                'cover_image_url': 'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.3'),
                'verified_photos': True,
                'response_time_minutes': 22,
                'completed_stays': 121,
                'cancellation_count': 1,
                'complaint_count': 2,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'emergency_ready': True,
                'near_transport': True,
                'supports_late_checkin': True,
                'workspace_ready': True,
                'family_friendly': True,
                'local_experience_bundle': 'Airport transfer + coworking pass',
            },
            {
                'name': 'OYO Comfort Inn Anna Nagar',
                'location': 'Chennai',
                'base_price': Decimal('3300.00'),
                'offer_price': Decimal('2199.00'),
                'description': 'Calm neighborhood hotel with family rooms, secure reception, and easy hospital access.',
                'cover_image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.2'),
                'verified_photos': True,
                'response_time_minutes': 35,
                'completed_stays': 84,
                'cancellation_count': 2,
                'complaint_count': 1,
                'is_women_friendly': True,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'emergency_ready': True,
                'supports_late_checkin': True,
                'family_friendly': True,
                'local_experience_bundle': 'Family breakfast bundle',
            },
            {
                'name': 'OYO Premium Lake View',
                'location': 'Udaipur',
                'base_price': Decimal('6100.00'),
                'offer_price': Decimal('4599.00'),
                'description': 'Leisure stay near the lake with spacious rooms, local tour assistance, and sunset views.',
                'cover_image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.7'),
                'verified_photos': True,
                'response_time_minutes': 40,
                'completed_stays': 175,
                'cancellation_count': 3,
                'complaint_count': 1,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'couple_friendly': True,
                'family_friendly': True,
                'local_experience_bundle': 'Lake tour + late checkout',
            },
            {
                'name': 'OYO Workpod Cyber Hub',
                'location': 'Gurugram',
                'base_price': Decimal('4800.00'),
                'offer_price': Decimal('3399.00'),
                'description': 'Business-first hotel with quiet rooms, desk setups, fast WiFi, and metro proximity.',
                'cover_image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.5'),
                'verified_photos': True,
                'response_time_minutes': 12,
                'completed_stays': 190,
                'cancellation_count': 1,
                'complaint_count': 0,
                'is_women_friendly': True,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'emergency_ready': True,
                'near_transport': True,
                'supports_late_checkin': True,
                'workspace_ready': True,
                'local_experience_bundle': 'Meeting room credit',
            },
            {
                'name': 'OYO Airport Express Stay',
                'location': 'Kolkata',
                'base_price': Decimal('3900.00'),
                'offer_price': Decimal('2699.00'),
                'description': 'Airport-side emergency stay with late check-in, verified staff, and fast pickup support.',
                'cover_image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.1'),
                'verified_photos': True,
                'response_time_minutes': 10,
                'completed_stays': 73,
                'cancellation_count': 1,
                'complaint_count': 1,
                'is_women_friendly': True,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'emergency_ready': True,
                'near_transport': True,
                'supports_late_checkin': True,
                'local_experience_bundle': 'Airport pickup on request',
            },
            {
                'name': 'OYO Heritage Courtyard',
                'location': 'Jaipur',
                'base_price': Decimal('4500.00'),
                'offer_price': Decimal('3099.00'),
                'description': 'Boutique heritage-style stay with verified photos, family rooms, and city guide support.',
                'cover_image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=80',
                'rating': Decimal('4.4'),
                'verified_photos': True,
                'response_time_minutes': 28,
                'completed_stays': 134,
                'cancellation_count': 2,
                'complaint_count': 0,
                'has_24x7_reception': True,
                'has_cctv': True,
                'has_verified_staff': True,
                'has_well_lit_area': True,
                'family_friendly': True,
                'couple_friendly': True,
                'local_experience_bundle': 'City guide + breakfast',
            },
        ]
        for spec in hotel_specs:
            hotel, created = Hotel.objects.get_or_create(
                name=spec['name'],
                defaults={
                    'vendor': vendor,
                    'location': spec['location'],
                    'address': f"{spec['location']} central business district",
                    'base_price': spec['base_price'],
                    'offer_price': spec['offer_price'],
                    'description': spec['description'],
                    'rating': spec['rating'],
                    'rooms_available': 18,
                },
            )
            for field, value in spec.items():
                if field != 'name':
                    setattr(hotel, field, value)
            hotel.save()
            hotel.amenities.set(amenities.values())
            HotelManager.objects.get_or_create(
                hotel=hotel,
                name='Front Desk',
                defaults={'contact_number': '011-4000-1000'},
            )

        self.stdout.write(self.style.SUCCESS('Demo data ready.'))
        self.stdout.write('Customer: customer@example.com / Password123!')
        self.stdout.write('Vendor: vendor@example.com / Password123!')
