# File: models.py
# Author: Anthony Xie (xiea@bu.edu)
# Date: December 9, 2024
# Description: Data models for the Travel Booking System application.
# Defines four interconnected models: Destination, TravelPackage, Customer, and Booking.

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Destination(models.Model):
    """
    Model representing a travel destination.
    This model can exist independently without foreign keys.
    """
    name = models.CharField(max_length=200, help_text="Name of the destination")
    country = models.CharField(max_length=100, help_text="Country where destination is located")
    description = models.TextField(help_text="Detailed description of the destination")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL to destination image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['country', 'name']

    def __str__(self):
        return f"{self.name}, {self.country}"


class TravelPackage(models.Model):
    """
    Model representing a travel package for a specific destination.
    References the Destination model via foreign key.
    """
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='packages',
        help_text="Destination for this travel package"
    )
    name = models.CharField(max_length=200, help_text="Name of the travel package")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price per person in USD"
    )
    start_date = models.DateField(help_text="Package start date")
    end_date = models.DateField(help_text="Package end date")
    duration_days = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Duration of the trip in days"
    )
    itinerary = models.TextField(help_text="Detailed day-by-day itinerary")
    available_spots = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of available spots for booking"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'destination']

    def __str__(self):
        return f"{self.name} - {self.destination.name}"

    def is_available(self):
        """Check if package has available spots"""
        return self.available_spots > 0


class Customer(models.Model):
    """
    Model representing a customer/user profile.
    This model can exist independently without foreign keys.
    """
    first_name = models.CharField(max_length=100, help_text="Customer's first name")
    last_name = models.CharField(max_length=100, help_text="Customer's last name")
    email = models.EmailField(unique=True, help_text="Customer's email address")
    phone = models.CharField(max_length=20, help_text="Customer's phone number")
    address = models.TextField(help_text="Customer's mailing address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Return the customer's full name"""
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    """
    Model representing a booking made by a customer for a travel package.
    References both Customer and TravelPackage models via foreign keys.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Customer who made the booking"
    )
    travel_package = models.ForeignKey(
        TravelPackage,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Travel package being booked"
    )
    booking_date = models.DateTimeField(auto_now_add=True, help_text="Date and time when booking was made")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the booking"
    )
    number_of_people = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of people in the booking"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Total price for the booking"
    )
    notes = models.TextField(blank=True, help_text="Additional notes or special requests")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.get_full_name()} - {self.travel_package.name}"

    def calculate_total_price(self):
        """Calculate total price based on number of people and package price"""
        return self.number_of_people * self.travel_package.price
