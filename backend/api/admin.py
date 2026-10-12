from django.contrib import admin
from .models import TourPackage, Booking, CustomTrip, Enquiry, LiveRate

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "price", "duration", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "slug", "description")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_id", "customer_name", "customer_phone", "package_title", "travel_date", "total_amount", "status", "created_at")
    list_filter = ("status", "source", "travel_date")
    search_fields = ("booking_id", "customer_name", "customer_phone", "customer_email")

@admin.register(CustomTrip)
class CustomTripAdmin(admin.ModelAdmin):
    list_display = ("trip_id", "contact_name", "contact_phone", "starting_city", "duration", "travelers_count", "status", "created_at")
    list_filter = ("status", "group_type", "duration")
    search_fields = ("trip_id", "contact_name", "contact_phone")

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("enquiry_id", "name", "phone", "destination", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("enquiry_id", "name", "phone", "email")

@admin.register(LiveRate)
class LiveRateAdmin(admin.ModelAdmin):
    list_display = ("package_title", "package_slug", "price", "duration", "updated_at")
