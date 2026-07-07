from decimal import Decimal

from django.db.models import Avg, Count, Q, Sum

from .models import Booking, Hotel


def attach_market_intelligence(hotels, purpose=''):
    hotels = list(hotels)
    if not hotels:
        return hotels

    avg_price = sum(hotel.offer_price for hotel in hotels) / len(hotels)
    for hotel in hotels:
        hotel.market_fairness = price_fairness_against_market(hotel, avg_price)
        hotel.match_score = stay_match_score(hotel, purpose)
    if purpose:
        hotels.sort(key=lambda hotel: hotel.match_score, reverse=True)
    return hotels


def price_fairness_against_market(hotel, avg_price):
    if avg_price <= 0:
        return hotel.price_fairness_label
    ratio = hotel.offer_price / avg_price
    if ratio <= Decimal('0.85') and hotel.rating >= 4:
        return 'Below market'
    if ratio <= Decimal('1.15'):
        return 'Fair vs market'
    return 'Above market'


def stay_match_score(hotel, purpose=''):
    score = 45
    score += min(hotel.trust_score // 5, 20)
    score += min(hotel.safety_score // 10, 10)
    if hotel.verified_photos:
        score += 5
    if hotel.rooms_available > 3:
        score += 5

    if purpose == 'work':
        score += 18 if hotel.workspace_ready else 0
        score += 7 if hotel.near_transport else 0
    elif purpose == 'family':
        score += 20 if hotel.family_friendly else 0
        score += 5 if hotel.rooms_available >= 5 else 0
    elif purpose == 'couple':
        score += 20 if hotel.couple_friendly else 0
        score += 5 if hotel.rating >= 4 else 0
    elif purpose == 'emergency':
        score += 18 if hotel.emergency_ready else 0
        score += 8 if hotel.has_24x7_reception else 0
        score += 6 if hotel.supports_late_checkin else 0
        score += 4 if hotel.near_transport else 0
    elif purpose == 'women_safe':
        score += min(hotel.safety_score // 2, 45)

    return max(0, min(score, 100))


def vendor_analytics(vendor):
    hotels = Hotel.objects.filter(vendor=vendor)
    bookings = Booking.objects.filter(hotel__vendor=vendor)
    confirmed = bookings.filter(status=Booking.Status.CONFIRMED)
    cancelled = bookings.filter(status=Booking.Status.CANCELLED)
    hotel_count = hotels.count()
    total_bookings = bookings.count()
    revenue = confirmed.aggregate(total=Sum('total_price'))['total'] or Decimal('0')
    avg_trust = hotels.aggregate(avg=Avg('rating'))['avg'] or 0
    top_hotel = (
        hotels.annotate(booking_count=Count('bookings', filter=Q(bookings__status=Booking.Status.CONFIRMED)))
        .order_by('-booking_count', '-rating')
        .first()
    )
    conversion_proxy = 0
    total_capacity = sum(hotel.rooms_available for hotel in hotels) or 1
    if hotel_count:
        conversion_proxy = min(int((confirmed.count() / total_capacity) * 100), 100)

    return {
        'hotel_count': hotel_count,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed.count(),
        'cancelled_bookings': cancelled.count(),
        'revenue': revenue,
        'avg_rating': round(float(avg_trust), 1),
        'top_hotel': top_hotel,
        'conversion_proxy': conversion_proxy,
    }
