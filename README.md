# OYO Clone - Django Hotel Booking System

A scalable hotel booking web application inspired by platforms like OYO, Agoda, and Airbnb. The project supports customer booking flows, vendor hotel management, image-backed hotel listings, smart stay matching, trust scoring, safety filters, and vendor analytics.

## Project Highlights

- Role-based authentication for customers and hotel vendors
- Hotel search by name, location, price range, amenities, trip purpose, safety, and emergency readiness
- Customer booking flow with date validation, overlap protection, booking history, and cancellation
- Vendor dashboard for hotel CRUD, image uploads, operational signals, and booking visibility
- Demo catalog with multiple Indian-city hotels and stock-photo cover images
- Django admin setup for users, hotels, amenities, images, managers, and bookings
- Seed command for instant demo data
- Focused tests for booking, role safety, matcher behavior, and filters

## Novel Features Compared To Normal Booking Apps

### 1. Trust Score

Each hotel gets a calculated Trust Score based on:

- Verified photos
- Rating
- Vendor response time
- Completed stays
- Complaint count
- Cancellation count

This helps users judge reliability instead of depending only on star ratings.

### 2. AI Stay Matcher

Users can choose their travel purpose:

- Work trip
- Family trip
- Couple stay
- Emergency tonight
- Women-safe stay

The app calculates a match percentage for every hotel using trust, safety, availability, and purpose-specific signals.

### 3. Smart Price Fairness

The system labels hotel pricing as:

- Below market
- Fair vs market
- Above market

This gives users a simple way to understand whether a listing is actually good value.

### 4. Women-Safe And Emergency Stay Modes

Hotels can be filtered by real operational signals:

- 24/7 reception
- CCTV in common areas
- Verified staff
- Well-lit location
- Late check-in support
- Emergency readiness

### 5. Vendor Analytics Dashboard

Vendors can see:

- Number of hotels
- Confirmed bookings
- Revenue
- Occupancy signal
- Average rating
- Top-performing hotel
- Trust and safety scores per property

## Tech Stack

- Python
- Django 5
- SQLite for local development
- Django templates
- CSS
- Pillow
- django-debug-toolbar
- python-decouple

## Folder Structure

```text
OYO/
├── accounts/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── hotels/
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   ├── views.py
│   └── management/commands/seed_demo.py
├── oyo_clone/
│   ├── settings.py
│   └── urls.py
├── static/css/app.css
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run migrations:

```powershell
python manage.py migrate
```

Load demo users and hotels:

```powershell
python manage.py seed_demo
```

Start the server:

```powershell
python manage.py runserver
```

Open the app:

```text
http://127.0.0.1:8000/
```

## Demo Accounts

```text
Customer
Email: customer@example.com
Password: Password123!

Vendor
Email: vendor@example.com
Password: Password123!
```

## Useful Routes

```text
/                         Hotel listing and search
/hotels/<slug>/           Hotel detail and booking
/bookings/                Customer bookings
/vendor/                  Vendor dashboard
/vendor/hotels/add/       Add hotel
/vendor/bookings/         Vendor booking analytics
/admin/                   Django admin
```

## Running Tests

```powershell
python manage.py test
```

## Demo Data

The `seed_demo` command creates:

- 1 customer account
- 1 vendor account
- Amenities like WiFi, Breakfast, Pool, Parking, Air conditioning, and Workspace
- 10 hotel listings across Delhi, Mumbai, Bengaluru, Hyderabad, Chennai, Udaipur, Gurugram, Kolkata, and Jaipur
- Trust, safety, emergency, workspace, family, and couple-friendly signals
- Stock-photo cover images for the hotel cards

## Image Credits

Hotel cover photos use externally hosted stock-photo URLs from Unsplash. Unsplash photos are generally free to use under the Unsplash license, with restrictions such as not reselling unmodified photos or building a competing photo service. See the Unsplash license details here:

https://unsplash.com/license

The project links to external image URLs for demo purposes instead of copying Pinterest or other copyrighted images into the repository.

## Notes

- The default email backend prints emails to the console for local development.
- SQLite is used for simplicity. PostgreSQL can be configured for production.
- Payment status is simulated as paid for demo purposes.
- The project is intended as an academic/portfolio implementation of a hotel booking system.
