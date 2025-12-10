# File: views.py
# Author: Anthony Xie (xiea@bu.edu)
# Date: December 9, 2024
# Description: View controllers for the Travel Booking System application.
# Implements CRUD operations using both function-based and class-based views,
# including search and filtering functionality.

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Destination, TravelPackage, Customer, Booking
from .forms import DestinationForm, TravelPackageForm, CustomerForm, BookingForm

# Home view
def home(request):
    """Home page showing overview of the travel booking system"""
    context = {
        'total_destinations': Destination.objects.count(),
        'total_packages': TravelPackage.objects.count(),
        'total_bookings': Booking.objects.count(),
        'featured_destinations': Destination.objects.all()[:3],
        'upcoming_packages': TravelPackage.objects.filter(available_spots__gt=0).order_by('start_date')[:4],
    }
    return render(request, 'project/home.html', context)


# Destination Views
class DestinationListView(ListView):
    """List all destinations"""
    model = Destination
    template_name = 'project/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        country_filter = self.request.GET.get('country', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if country_filter:
            queryset = queryset.filter(country__icontains=country_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['country_filter'] = self.request.GET.get('country', '')
        context['countries'] = Destination.objects.values_list('country', flat=True).distinct()
        return context


class DestinationDetailView(DetailView):
    """Show details of a specific destination"""
    model = Destination
    template_name = 'project/destination_detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['packages'] = self.object.packages.all()
        return context


class DestinationCreateView(CreateView):
    """Create a new destination"""
    model = Destination
    form_class = DestinationForm
    template_name = 'project/destination_form.html'
    success_url = reverse_lazy('destination-list')


class DestinationUpdateView(UpdateView):
    """Update an existing destination"""
    model = Destination
    form_class = DestinationForm
    template_name = 'project/destination_form.html'
    success_url = reverse_lazy('destination-list')


class DestinationDeleteView(DeleteView):
    """Delete a destination"""
    model = Destination
    template_name = 'project/destination_confirm_delete.html'
    success_url = reverse_lazy('destination-list')


# TravelPackage Views
class TravelPackageListView(ListView):
    """List all travel packages with filtering"""
    model = TravelPackage
    template_name = 'project/package_list.html'
    context_object_name = 'packages'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        destination_filter = self.request.GET.get('destination', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        available_only = self.request.GET.get('available_only', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(destination__name__icontains=search_query) |
                Q(itinerary__icontains=search_query)
            )

        if destination_filter:
            queryset = queryset.filter(destination_id=destination_filter)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if available_only:
            queryset = queryset.filter(available_spots__gt=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['destinations'] = Destination.objects.all()
        context['selected_destination'] = self.request.GET.get('destination', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['available_only'] = self.request.GET.get('available_only', '')
        return context


class TravelPackageDetailView(DetailView):
    """Show details of a specific travel package"""
    model = TravelPackage
    template_name = 'project/package_detail.html'
    context_object_name = 'package'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings'] = self.object.bookings.all()
        return context


class TravelPackageCreateView(CreateView):
    """Create a new travel package"""
    model = TravelPackage
    form_class = TravelPackageForm
    template_name = 'project/package_form.html'
    success_url = reverse_lazy('package-list')


class TravelPackageUpdateView(UpdateView):
    """Update an existing travel package"""
    model = TravelPackage
    form_class = TravelPackageForm
    template_name = 'project/package_form.html'
    success_url = reverse_lazy('package-list')


class TravelPackageDeleteView(DeleteView):
    """Delete a travel package"""
    model = TravelPackage
    template_name = 'project/package_confirm_delete.html'
    success_url = reverse_lazy('package-list')


# Customer Views
class CustomerListView(ListView):
    """List all customers"""
    model = Customer
    template_name = 'project/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class CustomerDetailView(DetailView):
    """Show details of a specific customer"""
    model = Customer
    template_name = 'project/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings'] = self.object.bookings.all()
        return context


class CustomerCreateView(CreateView):
    """Create a new customer"""
    model = Customer
    form_class = CustomerForm
    template_name = 'project/customer_form.html'
    success_url = reverse_lazy('customer-list')


class CustomerUpdateView(UpdateView):
    """Update an existing customer"""
    model = Customer
    form_class = CustomerForm
    template_name = 'project/customer_form.html'
    success_url = reverse_lazy('customer-list')


class CustomerDeleteView(DeleteView):
    """Delete a customer"""
    model = Customer
    template_name = 'project/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')


# Booking Views
class BookingListView(ListView):
    """List all bookings with filtering"""
    model = Booking
    template_name = 'project/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        customer_filter = self.request.GET.get('customer', '')

        if search_query:
            queryset = queryset.filter(
                Q(customer__first_name__icontains=search_query) |
                Q(customer__last_name__icontains=search_query) |
                Q(travel_package__name__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if customer_filter:
            queryset = queryset.filter(customer_id=customer_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_choices'] = Booking.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        context['customers'] = Customer.objects.all()
        context['selected_customer'] = self.request.GET.get('customer', '')
        return context


class BookingDetailView(DetailView):
    """Show details of a specific booking"""
    model = Booking
    template_name = 'project/booking_detail.html'
    context_object_name = 'booking'


class BookingCreateView(CreateView):
    """Create a new booking"""
    model = Booking
    form_class = BookingForm
    template_name = 'project/booking_form.html'
    success_url = reverse_lazy('booking-list')


class BookingUpdateView(UpdateView):
    """Update an existing booking"""
    model = Booking
    form_class = BookingForm
    template_name = 'project/booking_form.html'
    success_url = reverse_lazy('booking-list')


class BookingDeleteView(DeleteView):
    """Delete a booking"""
    model = Booking
    template_name = 'project/booking_confirm_delete.html'
    success_url = reverse_lazy('booking-list')
