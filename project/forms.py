from django import forms
from .models import Destination, TravelPackage, Customer, Booking


class DestinationForm(forms.ModelForm):
    """Form for creating and updating destinations"""

    class Meta:
        model = Destination
        fields = ['name', 'country', 'description', 'image_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter destination name'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter destination description'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
        }


class TravelPackageForm(forms.ModelForm):
    """Form for creating and updating travel packages"""

    class Meta:
        model = TravelPackage
        fields = ['destination', 'name', 'price', 'start_date', 'end_date', 'duration_days', 'itinerary', 'available_spots']
        widgets = {
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter package name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of days'}),
            'itinerary': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Day-by-day itinerary'}),
            'available_spots': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Available spots'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError('End date must be after start date.')

        return cleaned_data


class CustomerForm(forms.ModelForm):
    """Form for creating and updating customers"""

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '555-0100'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter mailing address'}),
        }


class BookingForm(forms.ModelForm):
    """Form for creating and updating bookings"""

    class Meta:
        model = Booking
        fields = ['customer', 'travel_package', 'status', 'number_of_people', 'total_price', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'travel_package': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of people'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes or special requests'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make total_price read-only for new bookings (can be overridden by admin)
        if not self.instance.pk:
            self.fields['total_price'].required = False
            self.fields['total_price'].help_text = 'Will be calculated automatically based on package price and number of people'

    def clean(self):
        cleaned_data = super().clean()
        travel_package = cleaned_data.get('travel_package')
        number_of_people = cleaned_data.get('number_of_people')

        if travel_package and number_of_people:
            # Check if enough spots are available
            if number_of_people > travel_package.available_spots:
                raise forms.ValidationError(
                    f'Only {travel_package.available_spots} spots available for this package.'
                )

            # Auto-calculate total price if not set
            if not cleaned_data.get('total_price'):
                cleaned_data['total_price'] = travel_package.price * number_of_people

        return cleaned_data
