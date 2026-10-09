# Spirit Adventures — Travel Agency Web Platform & Executive Admin Console

> **Explore the World, Without Limits.**  
> Comprehensive Documentation, Technical Architecture & Maintenance Guide.  
> **© Shaunak Kompalwar. All Rights Reserved.**

---

## 1. Brand & Project Overview

* **Brand Name:** Spirit Adventures
* **Headquarters / Office:** Vasantha Sai Apartments, Opposite Rishi Towers, KPHB, Kukatpally, Hyderabad – 500085
* **Contact Support:** +91 966 656 7551 | shaunakkompalwar968@gmail.com
* **Project Mission:** A modern, high-performance, mobile-responsive travel agency platform featuring interactive destination showcases, customizable tour planners, a real-time booking engine, and an executive SaaS administration dashboard with live synchronization and traffic analytics.

---

## 2. Technology Stack & Architecture

### Core Frontend Technologies
* **HTML5:** Semantic markup (`<nav>`, `<section>`, `<main>`, `<aside>`, `<footer>`, `<dialog>`), responsive media structures (`<video playsinline controls>`, vector SVGs).
* **CSS3 & Design Systems:**
  * **Layouts:** CSS Grid and Flexbox for responsive, adaptive multi-screen layouts.
  * **Design Aesthetic:** Dark-mode slate palette, Glassmorphism (`backdrop-filter: blur()`), glowing borders, and modern SaaS dashboard styling.
  * **CSS Custom Properties (`:root`):** Centralized design tokens for theming, typography, and color variables.
  * **Motion Design:** Smooth `@keyframes` animations, micro-interactions, responsive hover states, and live row flash highlights.
* **Vanilla JavaScript (ES6+):**
  * Modern ECMAScript without heavy framework overhead (lightning-fast execution, zero compilation or bundling required).
  * `async/await`, Promises, Fetch API, and reactive event listeners.

### Browser & Web APIs
* **BroadcastChannel API (`spirit_booking_sync`):**
  * Enables **real-time cross-tab, bidirectional data transmission**.
  * When a customer books on `package.html` or `booking.html`, the `admin.html` dashboard instantly catches the event, updates counters, plays a chime, and flashes the new row without page reloading.
* **Web Storage API (`localStorage` & `sessionStorage`):**
  * Persistent caching of reservations (`spirit_local_bookings`), custom live rates (`spirit_custom_packages`), visitor analytics (`spirit_visitor_stats`), SheetDB configuration, and sound preferences.
  * Cross-window storage synchronization listeners for real-time fallback.
* **Web Audio API (`AudioContext`, `OscillatorNode`, `GainNode`):**
  * Native in-browser dual-tone synthesizer producing incoming notification chimes (D5/A5 & D6 frequencies) without external audio files.
* **Blob & Object URL API (`Blob`, `URL.createObjectURL`):**
  * In-browser on-the-fly generation and instant downloading of Excel spreadsheets (`.csv`) with UTF-8 BOM encoding.
* **Clipboard API (`navigator.clipboard`):**
  * Click-to-copy booking Reference IDs with interactive UI feedback.
* **Navigation & Performance Timing API:**
  * Automatically detects browser reloads vs. first-time visits to seamlessly bypass the intro video upon reload.

### Backend, Cloud & Third-Party Integrations
* **SheetDB REST API (Google Sheets Backend):**
  * Connects booking submissions from customer pages directly into Google Sheets in real time.
* **Razorpay Payment Gateway:**
  * Integrated payment processing (`checkout.js`).
* **WhatsApp Business Click-to-Chat API:**
  * Deep-linked direct chat links (`https://wa.me/...`) with pre-composed booking confirmation messages.
* **Formspree AJAX:**
  * Asynchronous email inquiry delivery directly to management.
* **Unsplash CDN:**
  * High-definition travel destination photography.

### UI Libraries, Typography & Icons
* **Font Awesome 6.4.0 (CDN):** Vector icons for interface controls, actions, and badges.
* **Google Fonts:**
  * `Outfit`: Geometric executive SaaS font for dashboard layouts.
  * `Poppins`: Clean modern UI body typeface.
  * `Playfair Display`: High-end editorial serif display font.
  * `Caveat`: Handwritten accent font.

---

## 3. Project Structure & Page Directory

```
Spiritadventure/
│
├── index.html          # Main Customer Landing Portal & Showcase
├── package.html        # Tour Package Catalog with Real-Time Booking Modal
├── booking.html        # Direct Booking Portal Wizard with Live Calculator
├── customize.html      # Tailor-Made Custom Trip Planner & Inquiry Builder
├── admin.html          # Executive SaaS Admin Dashboard & Control Center
├── style.css           # Global Stylesheet, Components & Keyframe Animations
├── script.js           # Client-Side Interactivity & Chatbot Guide
├── tracker.js          # Cross-Device Real-Time Cloud Visitor Tracking Engine
├── Readme.md           # Platform Documentation & Architecture Guide
│
└── Assests/            # Static Media Assets
    ├── img/            # Brand Logos, Destination Photos, Gallery Images
    └── video/          # Opening Welcome Video & Background Media
```

---

## 4. Key Platform Features

### 🌟 Customer Experience
1. **Welcome Video Modal:** Auto-plays on first visit with tap-for-sound unmuting. Smart navigation detection automatically skips the video on page reloads.
2. **Interactive Photo Gallery:** High-definition destination cards with a full-screen Lightbox Zoom modal.
3. **Wall of Fame:** Verified traveler reviews with expandable smooth view toggles.
4. **AI Travel Guide Chatbot:** Interactive floating chat assistant answering questions about destinations, custom itineraries, and office hours.
5. **Tour Package Booking (`package.html`):** Explore Coorg, Goa, Hampi, Ooty, Wayanad, and Kerala packages, with instant booking forms that generate unique `#PK-XXXXXX` references.
6. **Direct Booking Wizard (`booking.html`):** Real-time pricing calculations based on travelers, package rates, and customized requests.
7. **Custom Trip Planner (`customize.html`):** Form to configure custom destinations, group sizes, vehicle preferences, and budget ranges (`#CT-XXXXXX`).

### ⚡ Executive Admin Dashboard (`admin.html`)
1. **Modern Sidebar SaaS Layout:** Fixed navigation sidebar with real-time sync status badge, core workspace tabs, and administrator profile.
2. **Multi-Source Booking Segregation:**
   * **Package Tours Section (`package.html`)**
   * **Direct Bookings Section (`booking.html`)**
   * **Custom Trip Inquiries Section (`customize.html`)**
   * **Unified Master Records Table**
3. **Live Sync Influx & Sound Notifications:** Cross-tab broadcasts trigger animated row flashes and native Web Audio synthesizer chimes.
4. **Real-Time Booking Creation Terminal:** Walk-in or phone reservation entry desk that broadcasts instantly across open client tabs.
5. **Live Rates Controller:** Adjust package base rates and durations directly from the admin panel; broadcasts live to customer booking forms.
6. **SheetDB Google Sheets Integration:** Dynamic endpoint configuration saving all client entries to Google Sheets.
7. **Dedicated Home Enquiries Intake (`index.html`):**
   * **Full Travel Parameter Intake:** Real-time intake for custom quote requests submitted via the expanded "Explore Now" enquiry modal on `index.html`.
   * **Dedicated Admin Section:** Dedicated card (`#section-enquiry`) with instant search, status filtering, and CSV export (`spirit_home_index_enquiries.csv`).
   * **Executive KPI Metric Row:** Real-time metrics for Total Bookings, Pending Review, Confirmed Tours, and **Pipeline Value** (total gross booking revenue).
8. **Universal Cross-Device Responsiveness:**
   * **Smart TVs & 4K Displays (`@media (min-width: 1920px)`, `2560px`, `3840px`):** Scaled typography, remote-friendly focus rings (`:focus-visible`), and balanced container max-widths.
   * **Laptops & Desktops (`1025px - 1919px`):** High-density executive layout with smooth hover interactions.
   * **Tablets (`768px - 1024px`):** Adaptive 2-column grids and touch-optimized navigation.
   * **Mobile Phones (`320px - 767px`):** Zero horizontal overflow, slide-out drawer sidebar, thumb-friendly tap targets, and scrollable modal dialogs.
9. **Client Actions:** One-click WhatsApp direct chat, phone calling, full details modal, live edit modal, and status updates (Pending, Confirmed, Completed, Cancelled).

---

## 5. Setup & Maintenance Guide

### How to Run Locally & Access Admin Console
1. No Node.js build process, compilers, or server installation required.
2. Open `index.html` in any modern web browser (Chrome, Edge, Firefox, Safari).
3. To access the admin console, open `admin.html`.
4. **Admin Portal Authentication:**
   * **Username:** `spirit_adventure`
   * **Password:** `spirit@12`
   * Features a pre-render security gate preventing unauthorized layout visibility, show/hide password toggle, session persistence, and one-click Logout.

### How to Configure SheetDB Google Sheets Backend
1. Go to [SheetDB.io](https://sheetdb.io/) and connect your Google Sheet.
2. Ensure your Google Sheet contains these header columns:
   ```
   booking_id | timestamp | name | phone | email | package | travel_date | travelers | pickup_city | total_amount | notes | status | source
   ```
3. Open `admin.html`, paste your SheetDB API URL into the **SheetDB Integration** card, and click **Save URL**.

### How to Update Tour Packages or Pricing
1. **Via Admin Panel (Live):** Click **Live Rates Manager** in `admin.html`, adjust the rates or durations, and click **Push Live Rates**.
2. **Via Code:** Open `package.html` or `booking.html`, search for `defaultLivePackages`, and update the titles and rates.

### How to Update Contact Information
* Open `index.html`, scroll to `<footer id="contact">`, and modify the address, phone number, or email address.
* Update WhatsApp links (`https://wa.me/919666567551`) across `index.html`, `booking.html`, and `admin.html` if the support number changes.

---

## 6. License & Credits

* **Author & Developer:** Shaunak Kompalwar
* **Project:** Spirit Adventures Web Platform
* **Copyright:** © 2026 Spirit Adventures. All Rights Reserved.
