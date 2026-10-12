from django.db import models
from django.utils import timezone
import random

def generate_booking_id(prefix="PK"):
    num = random.randint(100000, 999999)
    return f"#{prefix}-{num}"

class TourPackage(models.Model):
    slug = models.SlugField(max_length=100, unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    duration = models.CharField(max_length=100)
    price = models.IntegerField(default=4999, help_text="Base price in INR per person")
    hero_image = models.TextField()
    rating = models.CharField(max_length=60, default="★ 4.9 (180+ Reviews)")
    pickup_location = models.CharField(max_length=200, default="Hyderabad & Bangalore")
    stay_type = models.CharField(max_length=200, default="Premium Homestay & Resort")
    season = models.CharField(max_length=100, default="October to March")
    description = models.TextField()
    
    # Structured JSON data
    itinerary = models.JSONField(default=list, blank=True)
    spots = models.JSONField(default=list, blank=True)
    inclusions = models.JSONField(default=list, blank=True)
    exclusions = models.JSONField(default=list, blank=True)
    testimonial = models.JSONField(default=dict, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Tour Package"
        verbose_name_plural = "Tour Packages"

    def __str__(self):
        return f"{self.title} (Rs. {self.price})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    SOURCE_CHOICES = [
        ("package", "Package Portal"),
        ("direct", "Direct Wizard"),
        ("walkin", "Manual Walk-in / Terminal"),
    ]

    booking_id = models.CharField(max_length=50, unique=True, default=generate_booking_id)
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default="package")
    package_slug = models.CharField(max_length=100, blank=True)
    package_title = models.CharField(max_length=200, blank=True)
    
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=50)
    customer_email = models.EmailField(blank=True)
    
    travel_date = models.CharField(max_length=60)
    travelers_count = models.PositiveIntegerField(default=2)
    pickup_city = models.CharField(max_length=150, blank=True)
    total_amount = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.booking_id} - {self.customer_name} ({self.package_title or self.package_slug}) - Rs. {self.total_amount}"


class CustomTrip(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    trip_id = models.CharField(max_length=50, unique=True)
    destinations = models.JSONField(default=list)
    other_destinations = models.CharField(max_length=300, blank=True)
    starting_city = models.CharField(max_length=150)
    travel_date = models.CharField(max_length=60)
    duration = models.CharField(max_length=100)
    group_type = models.CharField(max_length=100)
    travelers_count = models.PositiveIntegerField(default=2)
    stay_category = models.CharField(max_length=100, default="Standard")
    vehicle_type = models.CharField(max_length=100, default="Tempo Traveller")
    estimated_budget = models.IntegerField(default=0)
    
    contact_name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=50)
    contact_email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Custom Trip Inquiry"
        verbose_name_plural = "Custom Trip Inquiries"

    def __str__(self):
        return f"{self.trip_id} - {self.contact_name} - {', '.join(self.destinations)}"


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("contacted", "Contacted"),
        ("converted", "Converted"),
        ("closed", "Closed"),
    ]

    enquiry_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    destination = models.CharField(max_length=200, blank=True)
    travel_date = models.CharField(max_length=60, blank=True)
    travelers_count = models.PositiveIntegerField(default=2)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Website Quick Enquiry"
        verbose_name_plural = "Website Quick Enquiries"

    def __str__(self):
        return f"{self.enquiry_id} - {self.name} ({self.destination})"


class LiveRate(models.Model):
    package_slug = models.CharField(max_length=100, unique=True)
    package_title = models.CharField(max_length=200)
    price = models.IntegerField()
    duration = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["package_title"]

    def __str__(self):
        return f"{self.package_title} -> Rs. {self.price} ({self.duration})"
