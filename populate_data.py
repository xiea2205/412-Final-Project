# File: populate_data.py
# Author: Anthony Xie (xiea@bu.edu)
# Date: December 9, 2024
# Description: Database population script for the Travel Booking System.
# Creates sample data including destinations, travel packages, customers, and bookings.
# Run with: python populate_data.py
import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_project.settings')
django.setup()

from project.models import Destination, TravelPackage, Customer, Booking
from django.contrib.auth.models import User

def populate_database():
    """Populate the database with sample data"""

    print("Starting to populate database...")

    # Create or update admin user with password
    print("\n1. Setting up admin user...")
    try:
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')
        admin.save()
        print("   Admin password set to: admin123")
    except User.DoesNotExist:
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("   Admin user created with password: admin123")

    # Create Destinations
    print("\n2. Creating destinations...")
    destinations_data = [
        {
            'name': 'Tokyo',
            'country': 'Japan',
            'description': 'Experience the vibrant blend of traditional and modern culture in Japan\'s bustling capital city. Visit ancient temples, enjoy world-class sushi, and explore the neon-lit streets of Shibuya and Shinjuku.',
            'image_url': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf'
        },
        {
            'name': 'Paris',
            'country': 'France',
            'description': 'The City of Light offers iconic landmarks like the Eiffel Tower, world-renowned museums including the Louvre, charming cafes, and exquisite French cuisine.',
            'image_url': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34'
        },
        {
            'name': 'Bali',
            'country': 'Indonesia',
            'description': 'A tropical paradise featuring stunning beaches, lush rice terraces, ancient temples, and a rich cultural heritage. Perfect for relaxation and adventure.',
            'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4'
        },
        {
            'name': 'New York City',
            'country': 'USA',
            'description': 'The city that never sleeps offers world-class museums, Broadway shows, iconic landmarks like the Statue of Liberty, and diverse neighborhoods to explore.',
            'image_url': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9'
        },
        {
            'name': 'Santorini',
            'country': 'Greece',
            'description': 'Famous for its white-washed buildings with blue domes, stunning sunsets, beautiful beaches, and excellent Mediterranean cuisine.',
            'image_url': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e'
        },
    ]

    destinations = []
    for dest_data in destinations_data:
        destination, created = Destination.objects.get_or_create(
            name=dest_data['name'],
            country=dest_data['country'],
            defaults={
                'description': dest_data['description'],
                'image_url': dest_data['image_url']
            }
        )
        destinations.append(destination)
        print(f"   {'Created' if created else 'Found'} destination: {destination}")

    # Create Travel Packages
    print("\n3. Creating travel packages...")
    packages_data = [
        {
            'destination': destinations[0],  # Tokyo
            'name': 'Tokyo Adventure Week',
            'price': Decimal('2499.00'),
            'start_date': date.today() + timedelta(days=30),
            'duration_days': 7,
            'itinerary': '''Day 1: Arrival in Tokyo, hotel check-in, evening walk in Shibuya
Day 2: Visit Senso-ji Temple, Akihabara electronics district
Day 3: Day trip to Mt. Fuji and Hakone
Day 4: Tsukiji Fish Market, Imperial Palace, Ginza shopping
Day 5: Harajuku, Meiji Shrine, teamLab Borderless
Day 6: Day trip to Nikko
Day 7: Last-minute shopping, departure''',
            'available_spots': 15
        },
        {
            'destination': destinations[0],  # Tokyo
            'name': 'Tokyo Food & Culture Tour',
            'price': Decimal('1899.00'),
            'start_date': date.today() + timedelta(days=45),
            'duration_days': 5,
            'itinerary': '''Day 1: Arrival, traditional kaiseki dinner
Day 2: Sushi making class, Tsukiji market tour
Day 3: Ramen museum, traditional tea ceremony
Day 4: Street food tour in Asakusa
Day 5: Last breakfast, departure''',
            'available_spots': 10
        },
        {
            'destination': destinations[1],  # Paris
            'name': 'Romantic Paris Getaway',
            'price': Decimal('2199.00'),
            'start_date': date.today() + timedelta(days=60),
            'duration_days': 6,
            'itinerary': '''Day 1: Arrival, Seine River cruise
Day 2: Eiffel Tower, Champs-Élysées
Day 3: Louvre Museum, Latin Quarter
Day 4: Versailles Palace day trip
Day 5: Montmartre, Sacré-Cœur
Day 6: Last-minute shopping, departure''',
            'available_spots': 20
        },
        {
            'destination': destinations[2],  # Bali
            'name': 'Bali Beach & Culture',
            'price': Decimal('1599.00'),
            'start_date': date.today() + timedelta(days=40),
            'duration_days': 8,
            'itinerary': '''Day 1: Arrival in Bali, beach resort check-in
Day 2: Ubud rice terraces, monkey forest
Day 3: Temple tour (Tanah Lot, Uluwatu)
Day 4: Snorkeling and water sports
Day 5: Traditional Balinese cooking class
Day 6: Spa day and relaxation
Day 7: Sunrise trek to Mt. Batur
Day 8: Departure''',
            'available_spots': 12
        },
        {
            'destination': destinations[3],  # NYC
            'name': 'New York City Explorer',
            'price': Decimal('1999.00'),
            'start_date': date.today() + timedelta(days=20),
            'duration_days': 5,
            'itinerary': '''Day 1: Arrival, Times Square, Broadway show
Day 2: Statue of Liberty, Ellis Island, 9/11 Memorial
Day 3: Central Park, Metropolitan Museum of Art
Day 4: Brooklyn Bridge, DUMBO, Williamsburg
Day 5: Last-minute shopping, departure''',
            'available_spots': 18
        },
    ]

    packages = []
    for pkg_data in packages_data:
        end_date = pkg_data['start_date'] + timedelta(days=pkg_data['duration_days'])
        package, created = TravelPackage.objects.get_or_create(
            name=pkg_data['name'],
            destination=pkg_data['destination'],
            defaults={
                'price': pkg_data['price'],
                'start_date': pkg_data['start_date'],
                'end_date': end_date,
                'duration_days': pkg_data['duration_days'],
                'itinerary': pkg_data['itinerary'],
                'available_spots': pkg_data['available_spots']
            }
        )
        packages.append(package)
        print(f"   {'Created' if created else 'Found'} package: {package}")

    # Create Customers
    print("\n4. Creating customers...")
    customers_data = [
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@email.com',
            'phone': '555-0101',
            'address': '123 Main St, Boston, MA 02101'
        },
        {
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'email': 'sarah.j@email.com',
            'phone': '555-0102',
            'address': '456 Oak Ave, Cambridge, MA 02138'
        },
        {
            'first_name': 'Michael',
            'last_name': 'Chen',
            'email': 'mchen@email.com',
            'phone': '555-0103',
            'address': '789 Elm St, Brookline, MA 02445'
        },
        {
            'first_name': 'Emily',
            'last_name': 'Williams',
            'email': 'emily.w@email.com',
            'phone': '555-0104',
            'address': '321 Pine Rd, Newton, MA 02458'
        },
        {
            'first_name': 'David',
            'last_name': 'Martinez',
            'email': 'david.m@email.com',
            'phone': '555-0105',
            'address': '654 Maple Dr, Somerville, MA 02143'
        },
    ]

    customers = []
    for cust_data in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=cust_data['email'],
            defaults={
                'first_name': cust_data['first_name'],
                'last_name': cust_data['last_name'],
                'phone': cust_data['phone'],
                'address': cust_data['address']
            }
        )
        customers.append(customer)
        print(f"   {'Created' if created else 'Found'} customer: {customer}")

    # Create Bookings
    print("\n5. Creating bookings...")
    bookings_data = [
        {
            'customer': customers[0],  # John Smith
            'package': packages[0],     # Tokyo Adventure Week
            'status': 'confirmed',
            'number_of_people': 2,
            'notes': 'Vegetarian meal preferences'
        },
        {
            'customer': customers[1],  # Sarah Johnson
            'package': packages[2],     # Romantic Paris Getaway
            'status': 'confirmed',
            'number_of_people': 2,
            'notes': 'Anniversary trip'
        },
        {
            'customer': customers[2],  # Michael Chen
            'package': packages[3],     # Bali Beach & Culture
            'status': 'pending',
            'number_of_people': 1,
            'notes': 'Solo traveler'
        },
        {
            'customer': customers[3],  # Emily Williams
            'package': packages[4],     # NYC Explorer
            'status': 'confirmed',
            'number_of_people': 4,
            'notes': 'Family trip with 2 children'
        },
        {
            'customer': customers[4],  # David Martinez
            'package': packages[1],     # Tokyo Food & Culture
            'status': 'pending',
            'number_of_people': 1,
            'notes': 'Interested in photography tours'
        },
    ]

    bookings = []
    for book_data in bookings_data:
        total_price = book_data['package'].price * book_data['number_of_people']
        booking, created = Booking.objects.get_or_create(
            customer=book_data['customer'],
            travel_package=book_data['package'],
            defaults={
                'status': book_data['status'],
                'number_of_people': book_data['number_of_people'],
                'total_price': total_price,
                'notes': book_data['notes']
            }
        )
        bookings.append(booking)
        print(f"   {'Created' if created else 'Found'} booking: {booking}")

    print("\n" + "="*60)
    print("Database population complete!")
    print("="*60)
    print("\nSummary:")
    print(f"  Destinations: {Destination.objects.count()}")
    print(f"  Travel Packages: {TravelPackage.objects.count()}")
    print(f"  Customers: {Customer.objects.count()}")
    print(f"  Bookings: {Booking.objects.count()}")
    print("\nAdmin login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nTo access the admin interface:")
    print("  1. Run: python manage.py runserver")
    print("  2. Open: http://127.0.0.1:8000/admin/")
    print("  3. Login with the credentials above")

if __name__ == '__main__':
    populate_database()
