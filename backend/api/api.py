import random
from typing import List, Optional
from datetime import datetime
from ninja import NinjaAPI, Query
from django.db import connection
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import TourPackage, Booking, CustomTrip, Enquiry, LiveRate
from .schemas import (
    HealthResponse,
    PackageOut,
    PackageIn,
    BookingCreateIn,
    BookingOut,
    StatusUpdateIn,
    CustomTripCreateIn,
    CustomTripOut,
    EnquiryCreateIn,
    EnquiryOut,
    LiveRateIn,
    LiveRateOut,
    AdminAuthIn,
    AdminAuthOut,
    AdminStatsOut,
)

api = NinjaAPI(
    title="Spirit Adventures API",
    version="1.0.0",
    description="Executive SaaS Travel Agency API powered by Django 5.x and Django Ninja with automatic DB fallback.",
    docs_url="/docs",
)

# ---------------------------------------------------------------------------
# 1. System & Health Check
# ---------------------------------------------------------------------------
@api.get("/health", response=HealthResponse, tags=["System"])
def health_check(request):
    """
    Returns active database engine (PostgreSQL or SQLite fallback) and server health.
    """
    engine = connection.vendor  # 'postgresql' or 'sqlite'
    return {
        "status": "healthy",
        "db_engine": engine,
        "timestamp": timezone.now().isoformat(),
        "version": "1.0.0",
    }

# ---------------------------------------------------------------------------
# 2. Tour Packages
# ---------------------------------------------------------------------------
@api.get("/packages", response=List[PackageOut], tags=["Packages"])
def list_packages(request, active_only: bool = True):
    """
    Retrieve all active tour packages.
    """
    qs = TourPackage.objects.all()
    if active_only:
        qs = qs.filter(is_active=True)
    return list(qs)

@api.get("/packages/{slug}", response=PackageOut, tags=["Packages"])
def get_package(request, slug: str):
    """
    Retrieve details for a single tour package by slug.
    """
    return get_object_or_404(TourPackage, slug=slug)

@api.post("/packages", response=PackageOut, tags=["Packages"])
def create_or_update_package(request, payload: PackageIn):
    """
    Create or update a tour package.
    """
    package, _ = TourPackage.objects.update_or_create(
        slug=payload.slug,
        defaults=payload.dict(),
    )
    return package

# ---------------------------------------------------------------------------
# 3. Bookings
# ---------------------------------------------------------------------------
@api.post("/bookings", response=BookingOut, tags=["Bookings"])
def create_booking(request, payload: BookingCreateIn):
    """
    Create a new booking (Package reservation, Direct Wizard, or Walk-in desk).
    Automatically generates Reference ID (#PK-XXXXXX / #BK-XXXXXX / #WALK-XXXXXX)
    and computes total amount if not explicitly provided.
    """
    source = payload.source or "package"
    rand_num = random.randint(100000, 999999)

    if source == "direct":
        prefix = "BK"
    elif source == "walkin":
        prefix = "WALK"
    else:
        prefix = "PK"

    booking_id = f"#{prefix}-{rand_num}"

    # Auto-resolve package title and price if slug provided
    package_title = payload.package_title or ""
    total = payload.total_amount or 0

    if payload.package_slug:
        try:
            pkg = TourPackage.objects.get(slug=payload.package_slug)
            if not package_title:
                package_title = pkg.title
            if total <= 0:
                total = pkg.price * (payload.travelers or 1)
        except TourPackage.DoesNotExist:
            pass

    booking = Booking.objects.create(
        booking_id=booking_id,
        source=source,
        package_slug=payload.package_slug or "",
        package_title=package_title,
        customer_name=payload.name,
        customer_phone=payload.phone,
        customer_email=payload.email or "",
        travel_date=payload.travel_date,
        travelers_count=payload.travelers or 2,
        pickup_city=payload.pickup_city or "",
        total_amount=total,
        notes=payload.notes or "",
        status="pending",
    )
    return booking

@api.get("/bookings", response=List[BookingOut], tags=["Bookings"])
def list_bookings(
    request,
    source: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    """
    List bookings with optional filtering by source (package, direct, walkin), status, and search query.
    """
    qs = Booking.objects.all()

    if source and source != "all":
        qs = qs.filter(source=source)

    if status and status != "all":
        qs = qs.filter(status=status)

    if search:
        search_terms = search.strip()
        qs = qs.filter(
            Q(booking_id__icontains=search_terms)
            | Q(customer_name__icontains=search_terms)
            | Q(customer_phone__icontains=search_terms)
            | Q(customer_email__icontains=search_terms)
            | Q(package_title__icontains=search_terms)
            | Q(pickup_city__icontains=search_terms)
        )

    return list(qs)

@api.patch("/bookings/{booking_id}/status", response=BookingOut, tags=["Bookings"])
def update_booking_status(request, booking_id: str, payload: StatusUpdateIn):
    """
    Update booking status (pending, confirmed, completed, cancelled).
    """
    clean_id = booking_id if booking_id.startswith("#") else f"#{booking_id}"
    booking = get_object_or_404(Booking, booking_id=clean_id)
    booking.status = payload.status.lower()
    booking.save()
    return booking

# ---------------------------------------------------------------------------
# 4. Custom Trip Planner
# ---------------------------------------------------------------------------
@api.post("/custom-trips", response=CustomTripOut, tags=["Custom Trips"])
def create_custom_trip(request, payload: CustomTripCreateIn):
    """
    Submit a tailor-made custom trip itinerary inquiry.
    Generates reference ID (#CT-XXXXXX).
    """
    rand_num = random.randint(100000, 999999)
    trip_id = f"#CT-{rand_num}"

    trip = CustomTrip.objects.create(
        trip_id=trip_id,
        destinations=payload.destinations,
        other_destinations=payload.other_destinations or "",
        starting_city=payload.starting_city,
        travel_date=payload.travel_date,
        duration=payload.duration,
        group_type=payload.group_type,
        travelers_count=payload.travelers or 2,
        stay_category=payload.stay_category or "Standard",
        vehicle_type=payload.vehicle_type or "Tempo Traveller",
        estimated_budget=payload.estimated_budget or 0,
        contact_name=payload.name,
        contact_phone=payload.phone,
        contact_email=payload.email or "",
        notes=payload.notes or "",
        status="pending",
    )
    return trip

@api.get("/custom-trips", response=List[CustomTripOut], tags=["Custom Trips"])
def list_custom_trips(
    request,
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    """
    List custom trip inquiries with optional status and text search filtering.
    """
    qs = CustomTrip.objects.all()

    if status and status != "all":
        qs = qs.filter(status=status)

    if search:
        search_terms = search.strip()
        qs = qs.filter(
            Q(trip_id__icontains=search_terms)
            | Q(contact_name__icontains=search_terms)
            | Q(contact_phone__icontains=search_terms)
            | Q(starting_city__icontains=search_terms)
        )

    return list(qs)

@api.patch("/custom-trips/{trip_id}/status", response=CustomTripOut, tags=["Custom Trips"])
def update_custom_trip_status(request, trip_id: str, payload: StatusUpdateIn):
    """
    Update custom trip status.
    """
    clean_id = trip_id if trip_id.startswith("#") else f"#{trip_id}"
    trip = get_object_or_404(CustomTrip, trip_id=clean_id)
    trip.status = payload.status.lower()
    trip.save()
    return trip

# ---------------------------------------------------------------------------
# 5. Website Quick Enquiries
# ---------------------------------------------------------------------------
@api.post("/enquiries", response=EnquiryOut, tags=["Enquiries"])
def create_enquiry(request, payload: EnquiryCreateIn):
    """
    Submit a website quick quote or explore inquiry (#ENQ-XXXXXX).
    """
    rand_num = random.randint(100000, 999999)
    enquiry_id = f"#ENQ-{rand_num}"

    enquiry = Enquiry.objects.create(
        enquiry_id=enquiry_id,
        name=payload.name,
        phone=payload.phone,
        email=payload.email or "",
        destination=payload.destination or "",
        travel_date=payload.travel_date or "",
        travelers_count=payload.travelers or 2,
        message=payload.message or "",
        status="pending",
    )
    return enquiry

@api.get("/enquiries", response=List[EnquiryOut], tags=["Enquiries"])
def list_enquiries(
    request,
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    """
    List website inquiries with optional status and search filtering.
    """
    qs = Enquiry.objects.all()

    if status and status != "all":
        qs = qs.filter(status=status)

    if search:
        search_terms = search.strip()
        qs = qs.filter(
            Q(enquiry_id__icontains=search_terms)
            | Q(name__icontains=search_terms)
            | Q(phone__icontains=search_terms)
            | Q(destination__icontains=search_terms)
        )

    return list(qs)

@api.patch("/enquiries/{enquiry_id}/status", response=EnquiryOut, tags=["Enquiries"])
def update_enquiry_status(request, enquiry_id: str, payload: StatusUpdateIn):
    """
    Update inquiry status.
    """
    clean_id = enquiry_id if enquiry_id.startswith("#") else f"#{enquiry_id}"
    enquiry = get_object_or_404(Enquiry, enquiry_id=clean_id)
    enquiry.status = payload.status.lower()
    enquiry.save()
    return enquiry

# ---------------------------------------------------------------------------
# 6. Admin Control Center & Analytics
# ---------------------------------------------------------------------------
@api.post("/admin/auth/login", response=AdminAuthOut, tags=["Admin"])
def admin_login(request, payload: AdminAuthIn):
    """
    Authenticate administrator credentials.
    Standard executive credentials: username 'spirit_adventure', password 'spirit@12'
    """
    if (payload.username == "spirit_adventure" and payload.password == "spirit@12") or \
       (payload.username == "admin" and payload.password == "spirit@12"):
        return {
            "success": True,
            "message": "Authentication successful. Welcome Executive Administrator.",
            "token": "token-spirit-adventures-session-2026",
            "username": payload.username,
        }
    return {
        "success": False,
        "message": "Invalid username or password. Please verify credentials.",
        "token": None,
        "username": None,
    }

@api.get("/admin/stats", response=AdminStatsOut, tags=["Admin"])
def get_admin_stats(request):
    """
    Return real-time KPI metrics for the Executive Dashboard.
    """
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status="pending").count()
    confirmed_bookings = Booking.objects.filter(status="confirmed").count()
    completed_bookings = Booking.objects.filter(status="completed").count()

    # Total pipeline value (sum of total_amount from confirmed + pending bookings)
    val_agg = Booking.objects.exclude(status="cancelled").aggregate(val=Sum("total_amount"))
    pipeline_value = val_agg["val"] or 0

    total_enquiries = Enquiry.objects.count()
    total_custom_trips = CustomTrip.objects.count()

    return {
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "confirmed_bookings": confirmed_bookings,
        "completed_bookings": completed_bookings,
        "pipeline_value": pipeline_value,
        "total_enquiries": total_enquiries,
        "total_custom_trips": total_custom_trips,
    }

@api.get("/admin/rates", response=List[LiveRateOut], tags=["Admin"])
def get_live_rates(request):
    """
    Get live package rates and durations.
    """
    return list(LiveRate.objects.all())

@api.post("/admin/rates", response=LiveRateOut, tags=["Admin"])
def update_live_rate(request, payload: LiveRateIn):
    """
    Push updated base price and duration for a tour package.
    Automatically syncs into TourPackage model if present.
    """
    rate, _ = LiveRate.objects.update_or_create(
        package_slug=payload.package_slug,
        defaults={
            "package_title": payload.package_title,
            "price": payload.price,
            "duration": payload.duration,
        },
    )

    # Sync to TourPackage if it exists
    TourPackage.objects.filter(slug=payload.package_slug).update(
        price=payload.price,
        duration=payload.duration,
    )

    return rate
