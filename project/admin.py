# File: admin.py
# Author: Anthony Xie (xiea@bu.edu)
# Date: December 9, 2024
# Description: Django admin interface configuration for the Travel Booking System.
# Customizes the admin panel for managing destinations, packages, customers, and bookings.

from django.contrib import admin
from .models import Destination, TravelPackage, Customer, Booking

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    """Admin interface for Destination model"""
    list_display = ['name', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['name', 'country', 'description']
    ordering = ['country', 'name']
    date_hierarchy = 'created_at'


@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    """Admin interface for TravelPackage model"""
    list_display = ['name', 'destination', 'price', 'start_date', 'end_date', 'duration_days', 'available_spots']
    list_filter = ['destination', 'start_date', 'created_at']
    search_fields = ['name', 'destination__name', 'itinerary']
    ordering = ['start_date', 'destination']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Package Information', {
            'fields': ('name', 'destination', 'price')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'duration_days')
        }),
        ('Details', {
            'fields': ('itinerary', 'available_spots')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model"""
    list_display = ['get_full_name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering = ['last_name', 'first_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Contact Details', {
            'fields': ('phone', 'address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin interface for Booking model"""
    list_display = ['id', 'customer', 'travel_package', 'booking_date', 'status', 'number_of_people', 'total_price']
    list_filter = ['status', 'booking_date', 'travel_package__destination']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email', 'travel_package__name']
    ordering = ['-booking_date']
    date_hierarchy = 'booking_date'
    readonly_fields = ['booking_date', 'updated_at']

    fieldsets = (
        ('Booking Information', {
            'fields': ('customer', 'travel_package', 'status')
        }),
        ('Details', {
            'fields': ('number_of_people', 'total_price', 'notes')
        }),
        ('Timestamps', {
            'fields': ('booking_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-calculate total price if not manually set"""
        if not change:  # Only for new bookings
            obj.total_price = obj.calculate_total_price()
        super().save_model(request, obj, form, change)
