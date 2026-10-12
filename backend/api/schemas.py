from typing import List, Optional, Any, Dict
from ninja import Schema
from datetime import datetime

class HealthResponse(Schema):
    status: str
    db_engine: str
    timestamp: str
    version: str = "1.0.0"

class ItineraryDay(Schema):
    day: str
    title: str
    meals: Optional[str] = None
    activities: List[str] = []

class SpotDetail(Schema):
    name: str
    tag: Optional[str] = None
    img: Optional[str] = None
    desc: Optional[str] = None
    food: Optional[str] = None
    activity: Optional[str] = None
    timing: Optional[str] = None
    tip: Optional[str] = None

class TestimonialItem(Schema):
    quote: str
    author: str

class PackageOut(Schema):
    slug: str
    title: str
    tagline: Optional[str] = ""
    duration: str
    price: int
    hero_image: str
    rating: Optional[str] = "★ 4.9 (180+ Reviews)"
    pickup_location: Optional[str] = "Hyderabad & Bangalore"
    stay_type: Optional[str] = "Premium Homestay & Resort"
    season: Optional[str] = "October to March"
    description: str
    itinerary: List[Dict[str, Any]] = []
    spots: List[Dict[str, Any]] = []
    inclusions: List[str] = []
    exclusions: List[str] = []
    testimonial: Optional[Dict[str, Any]] = None
    is_active: bool = True

class PackageIn(Schema):
    slug: str
    title: str
    tagline: Optional[str] = ""
    duration: str
    price: int
    hero_image: str
    rating: Optional[str] = "★ 4.9 (180+ Reviews)"
    pickup_location: Optional[str] = "Hyderabad & Bangalore"
    stay_type: Optional[str] = "Premium Homestay & Resort"
    season: Optional[str] = "October to March"
    description: str
    itinerary: Optional[List[Dict[str, Any]]] = []
    spots: Optional[List[Dict[str, Any]]] = []
    inclusions: Optional[List[str]] = []
    exclusions: Optional[List[str]] = []
    testimonial: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = True

class BookingCreateIn(Schema):
    source: Optional[str] = "package"
    package_slug: Optional[str] = ""
    package_title: Optional[str] = ""
    name: str
    phone: str
    email: Optional[str] = ""
    travel_date: str
    travelers: Optional[int] = 2
    pickup_city: Optional[str] = ""
    total_amount: Optional[int] = 0
    notes: Optional[str] = ""

class BookingOut(Schema):
    id: int
    booking_id: str
    source: str
    package_slug: str
    package_title: str
    customer_name: str
    customer_phone: str
    customer_email: str
    travel_date: str
    travelers_count: int
    pickup_city: str
    total_amount: int
    notes: str
    status: str
    created_at: datetime

class StatusUpdateIn(Schema):
    status: str

class CustomTripCreateIn(Schema):
    destinations: List[str]
    other_destinations: Optional[str] = ""
    starting_city: str
    travel_date: str
    duration: str
    group_type: str
    travelers: Optional[int] = 2
    stay_category: Optional[str] = "Standard"
    vehicle_type: Optional[str] = "Tempo Traveller"
    estimated_budget: Optional[int] = 0
    name: str
    phone: str
    email: Optional[str] = ""
    notes: Optional[str] = ""

class CustomTripOut(Schema):
    id: int
    trip_id: str
    destinations: List[str]
    other_destinations: str
    starting_city: str
    travel_date: str
    duration: str
    group_type: str
    travelers_count: int
    stay_category: str
    vehicle_type: str
    estimated_budget: int
    contact_name: str
    contact_phone: str
    contact_email: str
    notes: str
    status: str
    created_at: datetime

class EnquiryCreateIn(Schema):
    name: str
    phone: str
    email: Optional[str] = ""
    destination: Optional[str] = ""
    travel_date: Optional[str] = ""
    travelers: Optional[int] = 2
    message: Optional[str] = ""

class EnquiryOut(Schema):
    id: int
    enquiry_id: str
    name: str
    phone: str
    email: str
    destination: str
    travel_date: str
    travelers_count: int
    message: str
    status: str
    created_at: datetime

class LiveRateIn(Schema):
    package_slug: str
    package_title: str
    price: int
    duration: str

class LiveRateOut(Schema):
    package_slug: str
    package_title: str
    price: int
    duration: str
    updated_at: datetime

class AdminAuthIn(Schema):
    username: str
    password: str

class AdminAuthOut(Schema):
    success: bool
    message: str
    token: Optional[str] = None
    username: Optional[str] = None

class AdminStatsOut(Schema):
    total_bookings: int
    pending_bookings: int
    confirmed_bookings: int
    completed_bookings: int
    pipeline_value: int
    total_enquiries: int
    total_custom_trips: int
