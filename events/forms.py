from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event, TicketType, Ticket, EventImage, EventsLaunchNotification
from django.core.mail import send_mail
from django.conf import settings

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'category', 'description', 'main_image',
            'venue', 'address', 'city', 'country',
            'start_date', 'start_time', 'end_date', 'end_time',
            'max_capacity', 'registration_deadline',
            'website', 'contact_email', 'contact_phone',
            'status', 'is_featured'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'registration_deadline': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 5}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        registration_deadline = cleaned_data.get('registration_deadline')

        # Validate dates
        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date cannot be before start date")

        # Validate times for same-day events
        if (start_date and end_date and start_time and end_time and 
            start_date == end_date and start_time >= end_time):
            raise ValidationError("End time must be after start time for same-day events")

        # Validate registration deadline
        if registration_deadline:
            event_start = timezone.make_aware(
                timezone.datetime.combine(start_date, start_time)
            )
            if registration_deadline >= event_start:
                raise ValidationError(
                    "Registration deadline must be before event start time"
                )

        return cleaned_data

class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = [
            'name', 'description', 'price', 'quantity',
            'sales_start', 'sales_end',
            'max_tickets_per_order', 'min_tickets_per_order'
        ]
        widgets = {
            'sales_start': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'sales_end': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        sales_start = cleaned_data.get('sales_start')
        sales_end = cleaned_data.get('sales_end')
        min_tickets = cleaned_data.get('min_tickets_per_order')
        max_tickets = cleaned_data.get('max_tickets_per_order')

        if sales_start and sales_end and sales_start >= sales_end:
            raise ValidationError("Sales end time must be after sales start time")

        if min_tickets and max_tickets and min_tickets > max_tickets:
            raise ValidationError(
                "Minimum tickets per order cannot be greater than maximum"
            )

        return cleaned_data

class TicketPurchaseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['quantity', 'attendee_name', 'attendee_email', 'special_requirements']
        widgets = {
            'special_requirements': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.ticket_type = kwargs.pop('ticket_type', None)
        super().__init__(*args, **kwargs)
        
        if self.ticket_type:
            self.fields['quantity'].widget.attrs.update({
                'min': self.ticket_type.min_tickets_per_order,
                'max': self.ticket_type.max_tickets_per_order
            })

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if self.ticket_type:
            if quantity < self.ticket_type.min_tickets_per_order:
                raise ValidationError(
                    f"Minimum {self.ticket_type.min_tickets_per_order} tickets required"
                )
            if quantity > self.ticket_type.max_tickets_per_order:
                raise ValidationError(
                    f"Maximum {self.ticket_type.max_tickets_per_order} tickets allowed"
                )
            if quantity > self.ticket_type.tickets_remaining():
                raise ValidationError(
                    f"Only {self.ticket_type.tickets_remaining()} tickets available"
                )
        return quantity

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['image', 'caption', 'is_primary']

class EventSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search events...',
        'class': 'form-control'
    }))
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="All Categories"
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    city = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import EventCategory
        self.fields['category'].queryset = EventCategory.objects.all()

class LaunchNotificationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    
    class Meta:
        model = EventsLaunchNotification
        fields = ['email']