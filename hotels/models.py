from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify


class Amenity(models.Model):
    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(max_length=40, blank=True, help_text='Optional CSS/icon label.')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return self.name


class Hotel(models.Model):
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotels',
        limit_choices_to={'role': 'vendor'},
    )
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=180, db_index=True)
    address = models.TextField(blank=True)
    cover_image_url = models.URLField(blank=True)
    amenities = models.ManyToManyField(Amenity, related_name='hotels', blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    rooms_available = models.PositiveIntegerField(default=10)
    verified_photos = models.BooleanField(default=False)
    response_time_minutes = models.PositiveIntegerField(default=60)
    completed_stays = models.PositiveIntegerField(default=0)
    cancellation_count = models.PositiveIntegerField(default=0)
    complaint_count = models.PositiveIntegerField(default=0)
    is_women_friendly = models.BooleanField(default=False)
    has_24x7_reception = models.BooleanField(default=False)
    has_cctv = models.BooleanField(default=False)
    has_verified_staff = models.BooleanField(default=False)
    has_well_lit_area = models.BooleanField(default=False)
    emergency_ready = models.BooleanField(default=False)
    near_transport = models.BooleanField(default=False)
    supports_late_checkin = models.BooleanField(default=False)
    workspace_ready = models.BooleanField(default=False)
    family_friendly = models.BooleanField(default=False)
    couple_friendly = models.BooleanField(default=False)
    local_experience_bundle = models.CharField(max_length=180, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['location', 'is_active']),
            models.Index(fields=['offer_price']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hotel-detail', kwargs={'slug': self.slug})

    @property
    def primary_image(self):
        image = self.images.first()
        return image.image.url if image else self.cover_image_url

    @property
    def trust_score(self):
        score = 35
        score += min(int(float(self.rating) * 8), 40)
        if self.verified_photos:
            score += 10
        if self.response_time_minutes <= 30:
            score += 8
        elif self.response_time_minutes <= 90:
            score += 4
        score += min(self.completed_stays // 10, 8)
        score -= min(self.complaint_count * 6, 24)
        score -= min(self.cancellation_count * 3, 18)
        return max(0, min(score, 100))

    @property
    def trust_label(self):
        if self.trust_score >= 85:
            return 'Excellent'
        if self.trust_score >= 70:
            return 'Strong'
        if self.trust_score >= 55:
            return 'Moderate'
        return 'New/Needs review'

    @property
    def safety_score(self):
        checks = [
            self.is_women_friendly,
            self.has_24x7_reception,
            self.has_cctv,
            self.has_verified_staff,
            self.has_well_lit_area,
        ]
        return int((sum(1 for check in checks if check) / len(checks)) * 100)

    @property
    def price_fairness_label(self):
        discount = 0
        if self.base_price:
            discount = (self.base_price - self.offer_price) / self.base_price
        if discount >= 0.25 and self.rating >= 4:
            return 'Great value'
        if discount >= 0.10 or self.rating >= 4.3:
            return 'Fair price'
        return 'Premium'

    @property
    def reliability_summary(self):
        return f'{self.completed_stays} completed stays, {self.complaint_count} complaints'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 2
            while Hotel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotels/')
    caption = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f'Image for {self.hotel}'


class HotelManager(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='managers')
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} - {self.hotel.name}'


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'customer'},
    )
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONFIRMED)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PAID)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['hotel', 'start_date', 'end_date']),
            models.Index(fields=['customer', 'status']),
        ]

    def __str__(self):
        return f'{self.hotel.name} for {self.customer.email}'

    @property
    def nights(self):
        return max((self.end_date - self.start_date).days, 0)

    def clean(self):
        if self.start_date and self.start_date < date.today():
            raise ValidationError({'start_date': 'Check-in cannot be in the past.'})
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError({'end_date': 'Check-out must be after check-in.'})
        if self.hotel_id and self.customer_id and self.start_date and self.end_date:
            overlapping = Booking.objects.filter(
                hotel=self.hotel,
                customer=self.customer,
                status=self.Status.CONFIRMED,
            ).filter(Q(start_date__lt=self.end_date) & Q(end_date__gt=self.start_date))
            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)
            if overlapping.exists():
                raise ValidationError('You already have a booking for this hotel during those dates.')

# Create your models here.
