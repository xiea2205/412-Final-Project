from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Destination URLs
    path('destinations/', views.DestinationListView.as_view(), name='destination-list'),
    path('destinations/<int:pk>/', views.DestinationDetailView.as_view(), name='destination-detail'),
    path('destinations/create/', views.DestinationCreateView.as_view(), name='destination-create'),
    path('destinations/<int:pk>/update/', views.DestinationUpdateView.as_view(), name='destination-update'),
    path('destinations/<int:pk>/delete/', views.DestinationDeleteView.as_view(), name='destination-delete'),

    # Travel Package URLs
    path('packages/', views.TravelPackageListView.as_view(), name='package-list'),
    path('packages/<int:pk>/', views.TravelPackageDetailView.as_view(), name='package-detail'),
    path('packages/create/', views.TravelPackageCreateView.as_view(), name='package-create'),
    path('packages/<int:pk>/update/', views.TravelPackageUpdateView.as_view(), name='package-update'),
    path('packages/<int:pk>/delete/', views.TravelPackageDeleteView.as_view(), name='package-delete'),

    # Customer URLs
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer-create'),
    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer-update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer-delete'),

    # Booking URLs
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking-delete'),
]
