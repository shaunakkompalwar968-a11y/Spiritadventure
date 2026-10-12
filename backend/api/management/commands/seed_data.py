from django.core.management.base import BaseCommand
from api.models import TourPackage, Booking, CustomTrip, Enquiry, LiveRate

class Command(BaseCommand):
    help = "Seeds the database with tour packages, live rates, and demo bookings"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Spirit Adventures database...")

        packages_data = [
            {
                "slug": "coorg",
                "title": "Coorg Getaway",
                "tagline": "The Scotland of India • Misty Valleys, Coffee Plantations & Waterfalls",
                "duration": "2 Days, 1 Night",
                "price": 4999,
                "hero_image": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.9 (180+ Reviews)",
                "pickup_location": "Hyderabad & Bangalore",
                "stay_type": "Premium Coffee Estate Homestay & Resort",
                "season": "October to March",
                "description": "Escape into the tranquil, emerald hills of Coorg (Kodagu). Known affectionately as the 'Scotland of India,' Coorg offers refreshing mountain air, cascading silver waterfalls, and endless aromatic coffee and spice plantations. Our weekend package includes cozy estate accommodations, guided waterfall treks, authentic Kodava cuisine, and magical sunset viewpoints at Raja's Seat.",
                "itinerary": [
                    {
                        "day": "Day 1",
                        "title": "Arrival, Coffee Trails & Sunset Viewpoint",
                        "meals": "Campfire Dinner Included",
                        "activities": [
                            "Scenic morning drive through Western Ghats into Madikeri; check-in at our boutique coffee estate resort.",
                            "Guided walking tour through sprawling coffee and spice plantations; learn about coffee bean harvesting and roasting.",
                            "Visit the thundering Abbey Falls nestled deep inside private estates; photograph the falls from the iconic hanging bridge.",
                            "Witness a spectacular golden sunset at Raja's Seat overlooking endless rolling misty valleys.",
                            "Warm evening campfire with music and an authentic Kodava dinner feast."
                        ]
                    },
                    {
                        "day": "Day 2",
                        "title": "Gentle Giants, Golden Temple & Return Journey",
                        "meals": "Breakfast Included",
                        "activities": [
                            "Enjoy freshly brewed South Indian filter coffee made from estate beans, followed by a buffet breakfast.",
                            "Excursion to Dubare Elephant Camp on the Kaveri riverbanks; interact with gentle giants and witness river bathing.",
                            "Tour the majestic Namdroling Monastery (Golden Temple) in Bylakuppe with 40-foot gilded Buddha statues.",
                            "Shopping stop for authentic Coorg homemade chocolates, pure organic honey, and aromatic spices.",
                            "Depart on return journey back to Hyderabad / Bangalore with unforgettable memories."
                        ]
                    }
                ],
                "spots": [
                    {
                        "name": "Abbey Falls",
                        "tag": "Misty Waterfall",
                        "img": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
                        "desc": "A dramatic 70-foot waterfall roaring over massive granite boulders into a serene pool, enveloped by lush coffee estates and pepper vines.",
                        "food": "Hot spiced roasted sweet corn and traditional steamed Kadambuttu dumplings.",
                        "activity": "Hanging bridge stroll and mist photography.",
                        "timing": "Morning (8:30 AM – 11:00 AM) for gentle sunlight.",
                        "tip": "Wear slip-resistant sneakers for walking down the estate steps."
                    },
                    {
                        "name": "Raja's Seat",
                        "tag": "Sunset Point",
                        "img": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
                        "desc": "The historic garden viewpoint where the Kings of Kodagu spent evenings admiring spectacular sunsets over endless undulating green valleys.",
                        "food": "Hot Akki Roti with vegetable sagu and freshly brewed dark roast estate coffee.",
                        "activity": "Sunset gazing, musical fountain show, and valley photography.",
                        "timing": "Late afternoon through twilight (4:30 PM – 6:30 PM).",
                        "tip": "Arrive 30 minutes early to secure a prime spot at the heritage pavilion."
                    },
                    {
                        "name": "Dubare Elephant Camp",
                        "tag": "River Wildlife",
                        "img": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?auto=format&fit=crop&w=800&q=80",
                        "desc": "An eco-tourism camp situated on the banks of River Kaveri dedicated to elephant conservation, river bathing, and daily care.",
                        "food": "Traditional Malnad thali meal with tender bamboo shoot curry.",
                        "activity": "Elephant feeding, observing river bathing, and still-water boat crossing.",
                        "timing": "Early morning (9:00 AM – 11:00 AM).",
                        "tip": "Boat crossings fill up quickly; our tour manager coordinates prompt entry."
                    },
                    {
                        "name": "Namdroling Golden Temple",
                        "tag": "Tibetan Heritage",
                        "img": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
                        "desc": "The largest Tibetan Buddhist settlement in South India, featuring magnificent 40-foot gold-plated Buddha statues and ornate Tibetan artwork.",
                        "food": "Steamed Tibetan vegetable/chicken momos and steaming Thukpa noodle soup.",
                        "activity": "Temple prayer observation, peaceful meditation, and Tibetan handicrafts shopping.",
                        "timing": "10:00 AM – 4:30 PM.",
                        "tip": "Maintain silence inside the sanctum and remember to remove footwear before entering."
                    }
                ],
                "inclusions": [
                    "Round-trip transportation in comfortable AC Pushback Coach / Tempo Traveller",
                    "1 Night stay in certified boutique coffee estate resort / homestay",
                    "1 Delicious Breakfast and 1 Campfire Dinner feast included",
                    "Guided coffee and spice plantation walking tour with estate expert",
                    "All scheduled sightseeing in Madikeri, Dubare, and Bylakuppe",
                    "Evening campfire with acoustic music under starry skies",
                    "All highway tolls, inter-state vehicle taxes, and driver charges",
                    "24/7 dedicated Spirit Adventures tour coordinator on trip"
                ],
                "exclusions": [
                    "Personal expenses, shopping, and laundry service",
                    "Lunches during highway and sightseeing stops",
                    "Monument and monastery camera entry passes (if applicable)",
                    "River rafting or optional boating tickets at Dubare"
                ],
                "testimonial": {
                    "quote": "Great hospitality and service on our Coorg family trip. The estate stay amidst coffee plantations was surreal, and Abbey Falls was breathtaking. Everything went smoothly with our guide Sathvik!",
                    "author": "Avinash Bollaram — Verified Coorg Traveler"
                }
            },
            {
                "slug": "goa",
                "title": "Goa Beach Trip",
                "tagline": "Sun, Sand & Portuguese Charm • Water Sports, Forts & Vibrant Nightlife",
                "duration": "3 Days, 2 Nights",
                "price": 8500,
                "hero_image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.8 (240+ Reviews)",
                "pickup_location": "Hyderabad / Bangalore / Goa Airport",
                "stay_type": "3-Star Beach Resort with Swimming Pool",
                "season": "September to April",
                "description": "Feel the tropical breeze and soak in the vibrant coastal charm of Goa. From buzzing sandy shores in North Goa and exhilarating water sports to centuries-old Portuguese forts, Dudhsagar waterfalls, and laid-back sunset shacks, this 3 Days, 2 Nights holiday package provides the ultimate mix of thrill and beachside bliss.",
                "itinerary": [
                    {
                        "day": "Day 1",
                        "title": "Welcome to Goa & Baga Beach Sunset",
                        "meals": "Dinner Included",
                        "activities": [
                            "Arrival in Goa; pickup and check-in to our 3-star beach resort. Refresh by the pool.",
                            "Afternoon trip to Baga and Calangute beaches; relax on beach loungers with fresh coconut water.",
                            "Thrilling water sports session (Parasailing, Jet Ski, and Banana rides).",
                            "Explore vibrant beach shacks with live music, Goan seafood specials, and night market shopping."
                        ]
                    },
                    {
                        "day": "Day 2",
                        "title": "Heritage Forts, Latin Quarters & River Cruise",
                        "meals": "Breakfast Included",
                        "activities": [
                            "Buffet breakfast at resort followed by a visit to 17th-century Portuguese Fort Aguada and Lighthouse.",
                            "Explore the UNESCO World Heritage Basilica of Bom Jesus and Se Cathedral in Old Goa.",
                            "Stroll through the pastel-hued Portuguese Latin Quarter of Fontainhas in Panjim.",
                            "Scenic evening Mandovi River Cruise with live Goan folk dance performances and DJ music."
                        ]
                    },
                    {
                        "day": "Day 3",
                        "title": "Anjuna Cliffs, Bohemian Flea Markets & Departure",
                        "meals": "Breakfast Included",
                        "activities": [
                            "Breakfast and resort checkout; morning visit to scenic Anjuna and Vagator cliffs.",
                            "Visit Chapora Fort overlooking the Arabian Sea (famous 'Dil Chahta Hai' viewpoint).",
                            "Souvenir shopping at local Goan markets for cashew nuts, feni, and beachwear.",
                            "Drop-off at airport or railway station for return journey."
                        ]
                    }
                ],
                "spots": [
                    {
                        "name": "Baga & Calangute Beach",
                        "tag": "Sun & Water Sports",
                        "img": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
                        "desc": "Golden sands bustling with sunbeds, beachside shacks, and thrilling Arabian Sea water sports.",
                        "food": "Goan Fish/Prawn Curry with steamed rice and fresh coconut water.",
                        "activity": "Parasailing, jet ski, banana boat ride, and swimming.",
                        "timing": "10:00 AM – 6:00 PM for water sports.",
                        "tip": "Our team negotiates safe bundled water sport combos with certified life jackets."
                    },
                    {
                        "name": "Fort Aguada & Lighthouse",
                        "tag": "Portuguese Heritage",
                        "img": "https://images.unsplash.com/photo-1590523741831-ab7e8b8f9c7f?auto=format&fit=crop&w=800&q=80",
                        "desc": "A grand 17th-century coastal fortress standing proudly against the Arabian Sea, housing a freshwater spring and historic 4-tier lighthouse.",
                        "food": "Warm Goan Poee bread with Chicken Cafreal or Bebinca cake.",
                        "activity": "Rampart walks, panoramic ocean vistas, and heritage photography.",
                        "timing": "Late afternoon (3:30 PM – 5:30 PM) for softer coastal daylight.",
                        "tip": "Walk towards the lower ramparts for unobstructed ocean panoramas."
                    }
                ],
                "inclusions": [
                    "Round-trip airport / station transfers in AC vehicle",
                    "2 Nights stay in 3-star beachside resort with swimming pool",
                    "Daily morning buffet breakfast at resort",
                    "Guided North Goa & South Goa sightseeing tours",
                    "Evening Mandovi River Cruise ticket included",
                    "Assistance with discounted group water sports combos",
                    "All tolls, parking, and driver allowances"
                ],
                "exclusions": [
                    "Airfare / Train tickets to and from Goa",
                    "Optional water sports combo activity passes",
                    "Lunches and specialty club dinners",
                    "Personal bar expenses, laundry, and tips"
                ],
                "testimonial": {
                    "quote": "The water sports and beach parties organized by Spirit Adventures in Goa were top-notch! The resort was within walking distance to the beach, and our tour coordinator handled everything seamlessly.",
                    "author": "Priya Sharma — Verified Goa Traveler"
                }
            },
            {
                "slug": "hampi",
                "title": "Hampi, Gokarna & Dandeli",
                "tagline": "UNESCO Ruins, Sacred Coastlines & Whitewater Rapids • South India's Premier Circuit",
                "duration": "4 Days, 3 Nights",
                "price": 9500,
                "hero_image": "https://images.unsplash.com/photo-1600100397608-f010f443b785?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.9 (320+ Reviews)",
                "pickup_location": "Hyderabad & Bangalore",
                "stay_type": "Riverside Dandeli Jungle Resort & Beachside Gokarna Stay",
                "season": "September to March",
                "description": "The ultimate 3-in-1 adventure experience! Journey through the mystical boulder-strewn kingdom and monolithic temples of the Vijayanagara Empire in Hampi. Unwind on the serene, sacred cliffs of Om Beach in Gokarna, and conquer rushing whitewater rapids on the Kali River in Dandeli.",
                "itinerary": [
                    {
                        "day": "Day 1",
                        "title": "Monolithic Ruins & Sunset Over Hampi",
                        "meals": "Dinner Included",
                        "activities": [
                            "Early morning arrival in Hampi; check-in and fresh-up.",
                            "Explore the 7th-century Virupaksha Temple on the sacred banks of Tungabhadra River.",
                            "Visit the world-famous Vittala Temple Complex, Stone Chariot, and musical granite pillars.",
                            "Tour the Royal Enclosure, Lotus Mahal, and Elephant Stables.",
                            "Hike up Hemakuta Hill for an unforgettable golden sunset over the stone boulder kingdom; campfire dinner."
                        ]
                    },
                    {
                        "day": "Day 2",
                        "title": "Scenic Coastal Drive & Om Beach Gokarna",
                        "meals": "Breakfast & Beachside Dinner",
                        "activities": [
                            "Scenic morning drive from Hampi to the Arabian Sea coastline of Gokarna.",
                            "Visit the sacred Mahabaleshwar Temple with ancient Atmalinga heritage.",
                            "Explore naturally curved Om Beach; relax at cliffside cafes.",
                            "Sunset beach walk and campfire under starry coastal skies."
                        ]
                    },
                    {
                        "day": "Day 3",
                        "title": "Dandeli River Rafting & Jungle Adventures",
                        "meals": "Breakfast, Lunch & Barbecue Dinner",
                        "activities": [
                            "Morning drive into the dense teak and bamboo forests of Dandeli.",
                            "Kali River Whitewater Rafting, natural river jacuzzi, and river ziplining.",
                            "Check-in to riverside jungle resort; rain dance and pool party.",
                            "Jungle campfire with barbecue dinner."
                        ]
                    },
                    {
                        "day": "Day 4",
                        "title": "Supa Dam Canyon & Return Journey",
                        "meals": "Breakfast Included",
                        "activities": [
                            "Early morning jungle birdwatching and nature trail.",
                            "Buffet breakfast at resort.",
                            "Visit the grand Supa Dam canyon viewpoint and Syntheri Rocks monolith.",
                            "Afternoon departure on AC coach back to Hyderabad / Bangalore."
                        ]
                    }
                ],
                "spots": [
                    {
                        "name": "Virupaksha Temple & Ruins",
                        "tag": "Living UNESCO Heritage",
                        "img": "https://images.unsplash.com/photo-1600100397608-f010f443b785?auto=format&fit=crop&w=800&q=80",
                        "desc": "A 7th-century architectural wonder on the Tungabhadra River with an imposing 50-meter gopuram, active for over 1,300 years.",
                        "food": "Authentic South Indian thali, Benne Dosa & fresh tender coconut.",
                        "activity": "Coracle boat ride on Tungabhadra & temple architecture exploration.",
                        "timing": "Early morning (7:00 AM – 10:30 AM).",
                        "tip": "Notice the pinhole camera effect of the inverted gopuram shadow inside the temple."
                    },
                    {
                        "name": "Om Beach & Kudle Beach",
                        "tag": "Sacred Coastal Arc",
                        "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
                        "desc": "Naturally shaped in the sacred form of the Hindu Om symbol, fringed with rocky cliffs and azure Arabian Sea waves.",
                        "food": "Wood-fired pizzas at cliffside cafes, fresh grilled fish, and lemon ginger tea.",
                        "activity": "Cliff trekking, beach volleyball, ocean sunset swimming.",
                        "timing": "Twilight for ocean sunsets (3:30 PM – 6:45 PM).",
                        "tip": "Trek the scenic coastal path between Kudle and Om Beach for panoramic views."
                    }
                ],
                "inclusions": [
                    "Round-trip transportation in sanitized AC Pushback Coach",
                    "3 Nights comfortable stays (Hampi, Gokarna & Dandeli)",
                    "3 Breakfasts, 1 Lunch & 3 Campfire Dinners",
                    "Certified local history guide in Hampi",
                    "Kali river water activities (Natural Jacuzzi & Kayaking included)",
                    "Campfire nights with music in Hampi and Dandeli",
                    "All inter-state vehicle permits, tolls, and parking charges",
                    "24/7 dedicated Spirit Adventures tour coordinator"
                ],
                "exclusions": [
                    "Long-stretch Whitewater river rafting ticket (available as add-on)",
                    "Lunches in Hampi and Gokarna",
                    "Camera and monument entry fees",
                    "Personal adventure sports not listed in inclusions"
                ],
                "testimonial": {
                    "quote": "We traveled recently with Spirit Adventures for Gokarna and Dandeli. Our guide Sathwik was very friendly. The stay and food was very good, we enjoyed the pool and beachside stay!",
                    "author": "Shahid Ali — Verified Gokarna & Dandeli Traveler"
                }
            },
            {
                "slug": "ooty",
                "title": "Kodaikanal, Ooty & Mysore",
                "tagline": "The Queen of Hill Stations • Nilgiri Toy Train, Tea Plantations & Royal Palaces",
                "duration": "6 Days, 5 Nights",
                "price": 14000,
                "hero_image": "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.9 (290+ Reviews)",
                "pickup_location": "Hyderabad & Bangalore",
                "stay_type": "Heritage Hill Resorts in Ooty & Kodaikanal, 3-Star Mysore Hotel",
                "season": "Year-round (Peak: September to May)",
                "description": "Traverse the regal splendor of the Wadiyars in Mysore and ascend into the cool, misty paradise of the Nilgiri Hills. Ride the historic UNESCO mountain railway in Ooty, stroll through endless rolling emerald tea gardens in Coonoor, walk among giant ancient pine forests, and watch the illuminated brilliance of Mysore Palace.",
                "itinerary": [
                    {
                        "day": "Day 1",
                        "title": "Royal Mysore & Grand Palace Illumination",
                        "meals": "Dinner Included",
                        "activities": [
                            "Morning departure from Bangalore/Hyderabad; reach historic Mysore.",
                            "Visit Chamundi Hills and the sacred monolith Nandi Bull statue.",
                            "Guided tour of the grand Mysore Palace; admire royal artifacts.",
                            "Marvel at the breathtaking spectacle of Mysore Palace illuminated with 100,000 golden bulbs."
                        ]
                    },
                    {
                        "day": "Day 2",
                        "title": "Ascent to Ooty & Botanical Gardens",
                        "meals": "Breakfast & Dinner",
                        "activities": [
                            "Drive through Bandipur and Mudumalai Tiger Reserves up the 36 hairpin bends into Ooty.",
                            "Check-in to picturesque hill resort overlooking tea slopes.",
                            "Visit Government Botanical Garden featuring over 1,000 exotic flower species.",
                            "Evening boating on Ooty Lake surrounded by eucalyptus groves; chocolate tasting."
                        ]
                    }
                ],
                "spots": [
                    {
                        "name": "Mysore Grand Palace",
                        "tag": "Royal Heritage",
                        "img": "https://images.unsplash.com/photo-1600100397608-f010f443b782?auto=format&fit=crop&w=800&q=80",
                        "desc": "The official residence of the Wadiyar dynasty, boasting stained-glass domes, intricately carved teakwood ceilings, and royal armory.",
                        "food": "Authentic melt-in-the-mouth Mysore Pak & Mysore Masala Dosa.",
                        "activity": "Palace museum tour and evening golden illumination spectacle.",
                        "timing": "Illumination on Sundays & holidays (7:00 PM – 7:45 PM).",
                        "tip": "Socks are recommended inside the palace floors."
                    }
                ],
                "inclusions": [
                    "Round-trip AC Coach transfers",
                    "5 Nights accommodation in luxury hill resorts and 3-star hotel",
                    "Daily breakfast and dinners included",
                    "Toy train journey reservation assistance",
                    "All sightseeing in Mysore, Ooty, Coonoor, and Kodaikanal"
                ],
                "exclusions": [
                    "Toy train ticket cost (nominal)",
                    "Lunches and boating tickets",
                    "Camera tickets at botanical garden"
                ],
                "testimonial": {
                    "quote": "The Nilgiri views and Mysore palace lighting were completely magical. Spirit Adventures took care of our elderly parents with utmost care.",
                    "author": "Dr. Ramesh Varma — Verified Family Traveler"
                }
            },
            {
                "slug": "chikmagalur",
                "title": "Chikmagalur Coffee Trail",
                "tagline": "Mullayanagiri Peak, Emerald Coffee Estates & Bababudangiri",
                "duration": "2 Days, 1 Night",
                "price": 4499,
                "hero_image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.8 (150+ Reviews)",
                "pickup_location": "Hyderabad & Bangalore",
                "stay_type": "Hillside Estate Homestay",
                "season": "September to May",
                "description": "Breathe in the rejuvenating aroma of freshly blooming coffee blossoms and misty peaks. Trek to Mullayanagiri, the highest peak in Karnataka, explore hidden waterfalls, and unwind beside a crackling bonfire.",
                "itinerary": [
                    {
                        "day": "Day 1",
                        "title": "Mullayanagiri Peak & Waterfall Trek",
                        "meals": "Dinner & Bonfire Included",
                        "activities": [
                            "Morning arrival in Chikmagalur; check-in to hillside homestay.",
                            "Trek up Mullayanagiri Peak for jaw-dropping 360-degree panoramic views.",
                            "Visit picturesque Jhari Falls (Buttermilk Falls) via Jeep trail.",
                            "Campfire with Malnad barbecue specialties."
                        ]
                    },
                    {
                        "day": "Day 2",
                        "title": "Bababudangiri & Belur Temple Heritage",
                        "meals": "Breakfast Included",
                        "activities": [
                            "Sunrise walk through coffee gardens with birdwatching.",
                            "Visit sacred Bababudangiri hills and Manikyadhara falls.",
                            "Explore the historic Hoysala architecture of Chennakeshava Temple at Belur.",
                            "Return journey to Bangalore/Hyderabad."
                        ]
                    }
                ],
                "spots": [],
                "inclusions": ["AC Travel", "Homestay stay", "Breakfast & Dinner", "Campfire", "Trek coordination"],
                "exclusions": ["Jeep ride to Jhari falls (nominal ₹150)", "Lunch"],
                "testimonial": {
                    "quote": "Mullayanagiri trek was breathtaking! Very well organized weekend trip.",
                    "author": "Kavitha R."
                }
            },
            {
                "slug": "wayanad",
                "title": "Wayanad Nature Escape",
                "tagline": "Caves, Waterfalls, Bamboo Rafting & Chembra Peak Heart Lake",
                "duration": "3 Days, 2 Nights",
                "price": 5499,
                "hero_image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.9 (210+ Reviews)",
                "pickup_location": "Hyderabad & Bangalore",
                "stay_type": "Valley Resort with Infinity Pool",
                "season": "September to May",
                "description": "Discover God's Own Country in the forested highlands of Wayanad. See Neolithic rock carvings at Edakkal Caves, hike to the famous heart-shaped love lake at Chembra Peak, and cruise through bamboo groves on Kuruva Island.",
                "itinerary": [],
                "spots": [],
                "inclusions": ["AC Vehicle", "2 Nights Resort Stay", "Buffet Breakfasts", "Sightseeing"],
                "exclusions": ["Forest entry passes", "Lunches"],
                "testimonial": {
                    "quote": "Wayanad was serene and lush green. Spirit Adventures made the trip unforgettable!",
                    "author": "Rohit Verma"
                }
            },
            {
                "slug": "kerala",
                "title": "Kerala Backwaters & Hills",
                "tagline": "Alleppey Houseboat, Munnar Tea Valleys & Cochin Heritage",
                "duration": "5 Days, 4 Nights",
                "price": 8999,
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.9 (380+ Reviews)",
                "pickup_location": "Hyderabad / Bangalore / Cochin",
                "stay_type": "Deluxe Houseboat & Tea Valley Resort",
                "season": "Year-round",
                "description": "Cruising through tranquil palm-fringed canals in an authentic private Alleppey houseboat, sipping tender coconut water, and ascending the rolling green emerald tea hills of Munnar.",
                "itinerary": [],
                "spots": [],
                "inclusions": ["Private AC Houseboat with meals", "Munnar resort stay", "Transport & transfers", "Spice plantation tour"],
                "exclusions": ["Airfare/train", "Personal expenses"],
                "testimonial": {
                    "quote": "The Alleppey houseboat stay was a dream come true! Absolutely delicious Kerala meals on board.",
                    "author": "Sunita & Arvind Menon"
                }
            },
            {
                "slug": "dandeli",
                "title": "Dandeli River Rafting Adventure",
                "tagline": "Whitewater Rafting, Ziplining, Jacuzzi & Jungle Safari",
                "duration": "2 Days, 1 Night",
                "price": 4200,
                "hero_image": "https://images.unsplash.com/photo-1530866495561-507c9faab2ed?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.8 (190+ Reviews)",
                "pickup_location": "Hyderabad & Bangalore",
                "stay_type": "Riverside Adventure Camp / Resort",
                "season": "October to June",
                "description": "Get your adrenaline pumping on the rapids of the Kali River! Enjoy river crossing, coracle rides, natural jacuzzi baths, and deep jungle nature walks.",
                "itinerary": [],
                "spots": [],
                "inclusions": ["AC Travel", "Resort Stay", "All Meals", "Water Activities Included", "Night Campfire"],
                "exclusions": ["Long rafting stretch ticket (optional add-on)"],
                "testimonial": {
                    "quote": "Rafting in Dandeli was crazy fun! Sathwik and team took care of all safety gear.",
                    "author": "Ankit Gupta"
                }
            },
            {
                "slug": "gokarna",
                "title": "Gokarna Beach Trek",
                "tagline": "Cliff Trails, Kudle Beach, Om Beach & Bioluminescence",
                "duration": "2 Days, 1 Night",
                "price": 4600,
                "hero_image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.9 (175+ Reviews)",
                "pickup_location": "Hyderabad & Bangalore",
                "stay_type": "Beachfront Cottages / Tents",
                "season": "October to April",
                "description": "Trek across 5 pristine coastal beaches connected by scenic hilltops. Watch the sunset dip into the Arabian Sea from cliffside cafes, and sleep to the gentle sound of crashing ocean waves.",
                "itinerary": [],
                "spots": [],
                "inclusions": ["AC Sleeper/Pushback Coach", "Beach stay", "Breakfast & Dinner", "Guided Beach Trek"],
                "exclusions": ["Lunches & Cafe orders"],
                "testimonial": {
                    "quote": "The beach trek from Belekan to Om beach was scenic beyond words!",
                    "author": "Meera Nair"
                }
            },
            {
                "slug": "munnar",
                "title": "Munnar Tea Gardens",
                "tagline": "Misty Clouds, Anamudi Peak & Tea Museum Heritage",
                "duration": "3 Days, 2 Nights",
                "price": 6500,
                "hero_image": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1600&q=80",
                "rating": "★ 4.8 (140+ Reviews)",
                "pickup_location": "Hyderabad / Bangalore / Kochi",
                "stay_type": "Luxury Hilltop Resort",
                "season": "Year-round",
                "description": "Witness endless horizons of manicured tea plantations shrouded in silver mist. Visit Mattupetty Dam, Echo Point, and the Tata Tea Museum.",
                "itinerary": [],
                "spots": [],
                "inclusions": ["AC Vehicle", "2 Nights Resort", "Buffet Breakfasts", "Full Sightseeing"],
                "exclusions": ["Boating fees", "Lunches"],
                "testimonial": {
                    "quote": "The cold mist and tea gardens in Munnar were pure bliss.",
                    "author": "Siddharth Rao"
                }
            }
        ]

        # Seed Tour Packages
        for p in packages_data:
            obj, created = TourPackage.objects.update_or_create(
                slug=p["slug"],
                defaults=p,
            )
            status_str = "Created" if created else "Updated"
            self.stdout.write(f"  [{status_str}] Package: {obj.title} (Rs. {obj.price})")

            # Also ensure LiveRate exists
            LiveRate.objects.update_or_create(
                package_slug=p["slug"],
                defaults={
                    "package_title": p["title"],
                    "price": p["price"],
                    "duration": p["duration"],
                }
            )

        # Seed Sample Bookings
        demo_bookings = [
            {
                "booking_id": "#PK-829142",
                "source": "package",
                "package_slug": "coorg",
                "package_title": "Coorg Getaway",
                "customer_name": "Rahul Verma",
                "customer_phone": "+91 98765 43210",
                "customer_email": "rahul.verma@gmail.com",
                "travel_date": "2026-10-24",
                "travelers_count": 2,
                "pickup_city": "Hyderabad",
                "total_amount": 9998,
                "notes": "Prefer ground floor room in estate homestay.",
                "status": "confirmed",
            },
            {
                "booking_id": "#PK-319402",
                "source": "package",
                "package_slug": "goa",
                "package_title": "Goa Beach Trip",
                "customer_name": "Pooja Reddy",
                "customer_phone": "+91 91234 56789",
                "customer_email": "pooja.reddy@yahoo.com",
                "travel_date": "2026-11-05",
                "travelers_count": 4,
                "pickup_city": "Bangalore",
                "total_amount": 34000,
                "notes": "Group of 4 friends; please arrange poolside rooms.",
                "status": "pending",
            },
            {
                "booking_id": "#BK-401928",
                "source": "direct",
                "package_slug": "hampi",
                "package_title": "Hampi, Gokarna & Dandeli",
                "customer_name": "Siddharth Joshi",
                "customer_phone": "+91 98450 12345",
                "customer_email": "siddharth.j@outlook.com",
                "travel_date": "2026-10-30",
                "travelers_count": 3,
                "pickup_city": "Hyderabad",
                "total_amount": 28500,
                "notes": "Vegetarian meals requested during camping.",
                "status": "confirmed",
            },
            {
                "booking_id": "#WALK-10294",
                "source": "walkin",
                "package_slug": "ooty",
                "package_title": "Kodaikanal, Ooty & Mysore",
                "customer_name": "Vikram Adithya",
                "customer_phone": "+91 99887 76655",
                "customer_email": "vikram.adithya@gmail.com",
                "travel_date": "2026-11-12",
                "travelers_count": 2,
                "pickup_city": "KPHB Hyderabad Desk",
                "total_amount": 28000,
                "notes": "Walk-in reservation at KPHB office; paid token advance.",
                "status": "confirmed",
            },
            {
                "booking_id": "#BK-771290",
                "source": "direct",
                "package_slug": "chikmagalur",
                "package_title": "Chikmagalur Coffee Trail",
                "customer_name": "Ananya Sen",
                "customer_phone": "+91 97654 32109",
                "customer_email": "ananya.sen@gmail.com",
                "travel_date": "2026-10-18",
                "travelers_count": 2,
                "pickup_city": "Bangalore",
                "total_amount": 8998,
                "notes": "Celebrating wedding anniversary.",
                "status": "completed",
            }
        ]

        for b in demo_bookings:
            Booking.objects.update_or_create(
                booking_id=b["booking_id"],
                defaults=b,
            )
        self.stdout.write(f"  [Created] {len(demo_bookings)} Demo Bookings")

        # Seed Sample Custom Trips
        demo_custom_trips = [
            {
                "trip_id": "#CT-502914",
                "destinations": ["Coorg", "Wayanad"],
                "other_destinations": "Kabini Jungle Safari",
                "starting_city": "Hyderabad",
                "travel_date": "2026-11-15",
                "duration": "4 Days, 3 Nights",
                "group_type": "Family with Kids",
                "travelers_count": 5,
                "stay_category": "Luxury Homestay",
                "vehicle_type": "Tempo Traveller",
                "estimated_budget": 45000,
                "contact_name": "Karthik Raghavan",
                "contact_phone": "+91 94401 23456",
                "contact_email": "karthik.raghavan@techcorp.com",
                "notes": "Need child-friendly rooms and private campfire each night.",
                "status": "pending",
            },
            {
                "trip_id": "#CT-782103",
                "destinations": ["Gokarna", "Dandeli"],
                "other_destinations": "Murudeshwar Temple & Beach",
                "starting_city": "Bangalore",
                "travel_date": "2026-12-01",
                "duration": "3 Days, 2 Nights",
                "group_type": "Friends Group",
                "travelers_count": 8,
                "stay_category": "Standard",
                "vehicle_type": "Tempo Traveller",
                "estimated_budget": 52000,
                "contact_name": "Divya Murthy",
                "contact_phone": "+91 98860 65432",
                "contact_email": "divya.murthy@gmail.com",
                "notes": "College batch reunion. River rafting is compulsory.",
                "status": "confirmed",
            }
        ]

        for ct in demo_custom_trips:
            CustomTrip.objects.update_or_create(
                trip_id=ct["trip_id"],
                defaults=ct,
            )
        self.stdout.write(f"  [Created] {len(demo_custom_trips)} Demo Custom Trips")

        # Seed Sample Enquiries
        demo_enquiries = [
            {
                "enquiry_id": "#ENQ-104928",
                "name": "Suresh Babu",
                "phone": "+91 99490 88776",
                "email": "suresh.babu@gmail.com",
                "destination": "Goa & Dandeli",
                "travel_date": "2026-11-20",
                "travelers_count": 6,
                "message": "Corporate team outing for 6 developers. Looking for adventure activities and resort with conference space.",
                "status": "pending",
            },
            {
                "enquiry_id": "#ENQ-209481",
                "name": "Deepa Chandran",
                "phone": "+91 98200 11223",
                "email": "deepa.c@gmail.com",
                "destination": "Kerala Backwaters",
                "travel_date": "2026-12-25",
                "travelers_count": 2,
                "message": "Christmas vacation package quote for couple.",
                "status": "contacted",
            }
        ]

        for enq in demo_enquiries:
            Enquiry.objects.update_or_create(
                enquiry_id=enq["enquiry_id"],
                defaults=enq,
            )
        self.stdout.write(f"  [Created] {len(demo_enquiries)} Demo Enquiries")

        self.stdout.write(self.style.SUCCESS("Spirit Adventures database seeded successfully!"))
