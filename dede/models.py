from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from pyuploadcare.dj.models import ImageField
from django.utils import timezone
import random
from django.core.exceptions import ValidationError


class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    
    # Main image and gallery
    main_image = ImageField(blank=False, null=True, manual_crop="4:4",)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Tour(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tours')
    name = models.CharField(max_length=200)
    Image = ImageField(blank=True, null=True, manual_crop="4:4")  # Main tour image
    gallery_image1 = ImageField(blank=True, null=True, manual_crop="4:4")
    gallery_image2 = ImageField(blank=True, null=True, manual_crop="4:4")
    gallery_image3 = ImageField(blank=True, null=True, manual_crop="4:4")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    group_size = models.IntegerField(blank=True, null=True, default=30)
    languages = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, 
                               validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviews_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
   
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.destination.name} - {self.name}"

class TourHighlight(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='highlights')
    highlight = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.tour.name} - {self.highlight}"

class TourInclusion(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='inclusions')
    item = models.CharField(max_length=200)
    is_included = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.tour.name} - {self.item}"

class TourDay(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour_days')
    day_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    class Meta:
        ordering = ['day_number']
        
    def __str__(self):
        return f"{self.tour.name} - Day {self.day_number}"

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2,
                               validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Category ratings
    location_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    price_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    amenities_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    services_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rooms_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    def __str__(self):
        return f"{self.tour.name} - {self.user_name}"


class DayTrip(models.Model):
    RECURRENCE_CHOICES = (
        ('none', 'One-time Trip'),
        ('weekend', 'Every Weekend'),
        ('saturday', 'Every Saturday'),
        ('sunday', 'Every Sunday'),
    )

    # Basic Information
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    Image = ImageField(blank=True, null=True, manual_crop="16:9")
    gallery_image1 = ImageField(blank=True, null=True, manual_crop="4:4")
    gallery_image2 = ImageField(blank=True, null=True, manual_crop="4:4")
    gallery_image3 = ImageField(blank=True, null=True, manual_crop="4:4")
    
    # Date and Recurrence
    start_date = models.DateField(help_text="Start date for recurring trips or the date for one-time trips")
    end_date = models.DateField(null=True, blank=True, help_text="End date for recurring trips (optional)")
    description = models.TextField(blank=True)
    recurrence = models.CharField(
        max_length=20,
        choices=RECURRENCE_CHOICES,
        default='none',
        help_text="Select if this is a recurring trip"
    )
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    group_size = models.IntegerField(default=30, help_text="Maximum number of participants")
    
    # Pickup Information
    pickup_location = models.CharField(max_length=200)
    pickup_time = models.TimeField()
    
    # What's Included
    included_items = models.ManyToManyField('IncludedItem')
    
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_available_dates(self, num_weeks=8):
        """Return available dates for the next num_weeks based on recurrence pattern"""
        from datetime import datetime, timedelta
        available_dates = []
        today = timezone.now().date()
        end_date = self.end_date or today + timedelta(weeks=num_weeks)

        current_date = max(self.start_date, today)

        while current_date <= end_date:
            if self.recurrence == 'none':
                if self.start_date >= today:
                    available_dates.append(self.start_date)
                break
            elif self.recurrence == 'weekend':
                if current_date.weekday() in [5, 6]:  # Saturday = 5, Sunday = 6
                    available_dates.append(current_date)
            elif self.recurrence == 'saturday' and current_date.weekday() == 5:
                available_dates.append(current_date)
            elif self.recurrence == 'sunday' and current_date.weekday() == 6:
                available_dates.append(current_date)
            
            current_date += timedelta(days=1)

        return available_dates

    def get_remaining_slots(self, date=None):
        """Get remaining slots for a specific date"""
        # Default group size if not specified
        if date is None:
            date = timezone.now().date()
            
        total_booked = self.bookings.filter(
            travel_date=date,
            booking_status__in=['pending', 'confirmed']
        ).aggregate(
            total=models.Sum('number_of_people')
        )['total'] or 0
        
        return self.group_size - total_booked

    def is_available_on_date(self, check_date):
        """Check if the trip is available on a specific date"""
        if self.recurrence == 'none':
            return check_date == self.start_date
        
        if self.end_date and check_date > self.end_date:
            return False
            
        if check_date < self.start_date:
            return False
            
        if self.recurrence == 'weekend':
            return check_date.weekday() in [5, 6]
        elif self.recurrence == 'saturday':
            return check_date.weekday() == 5
        elif self.recurrence == 'sunday':
            return check_date.weekday() == 6
            
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.recurrence == 'none':
            return f"{self.name} - {self.start_date}"
        return f"{self.name} - {self.get_recurrence_display()}"

    class Meta:
        ordering = ['start_date']
        
class ItineraryItem(models.Model):
    daytrip = models.ForeignKey(DayTrip, on_delete=models.CASCADE, related_name='itinerary_items')
    time = models.TimeField()
    activity = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'time']

    def __str__(self):
        return f"{self.time.strftime('%H:%M')} - {self.activity}"

class IncludedItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For emoji or icon

    def __str__(self):
        return self.name

class OptionalActivity(models.Model):
    daytrip = models.ForeignKey(DayTrip, on_delete=models.CASCADE, related_name='optional_activities')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Optional Activities"

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    number_of_people = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Number of people must be at least 1"),
            MaxValueValidator(1000, message="Number of people cannot exceed 1000")  # or any reasonable maximum
        ]
    )
    
    # Customer information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    special_requirements = models.TextField(blank=True, null=True)

    # Booking details
    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Payment information
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )
    deposit_paid = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    
    # Additional information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Generate unique booking reference if not exists
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        super().save(*args, **kwargs)

    def generate_booking_reference(self):
        # Generate a unique booking reference based on timestamp and random numbers
        timestamp = timezone.now().strftime('%Y%m%d%H%M')
        random_nums = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f'BK{timestamp}{random_nums}'

    def calculate_total_price(self):
        return self.tour.price * self.number_of_people

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.tour.name} for {self.full_name}"

    def get_remaining_payment(self):
        return self.total_price - self.deposit_paid

    def is_fully_paid(self):
        return self.payment_status == 'paid'

    def can_be_cancelled(self):
        return self.booking_status not in ['completed', 'cancelled']

class DayTripBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    daytrip = models.ForeignKey(DayTrip, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    number_of_people = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Number of people must be at least 1"),
            MaxValueValidator(1000, message="Number of people cannot exceed 1000")
        ]
    )

    
    # Customer information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    special_requirements = models.TextField(blank=True, null=True)
    optional_activities = models.ManyToManyField('OptionalActivity', blank=True)

    # Booking details
    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Payment information
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )
    deposit_paid = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    
    # Additional information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Day Trip Booking"
        verbose_name_plural = "Day Trip Bookings"

    def clean(self):
        # Validate number of people against available slots
        if self.daytrip:
            remaining_slots = self.daytrip.get_remaining_slots()
            if self.number_of_people > remaining_slots:
                raise ValidationError(f"Only {remaining_slots} slots available for this day trip.")

    def save(self, *args, **kwargs):
        # Generate unique booking reference if not exists
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        
        # Set travel date from daytrip
        if not self.travel_date:
            self.travel_date = self.daytrip.date

        # Calculate total price if not set
        if not self.total_price:
            self.total_price = self.calculate_total_price()

        super().save(*args, **kwargs)

    def generate_booking_reference(self):
        # Generate a unique booking reference based on timestamp and random numbers
        timestamp = timezone.now().strftime('%Y%m%d%H%M')
        random_nums = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f'DT{timestamp}{random_nums}'

    def calculate_total_price(self):
        return self.daytrip.price * self.number_of_people

    def __str__(self):
        return f"Day Trip Booking {self.booking_reference} - {self.daytrip.name} for {self.full_name}"

    def get_remaining_payment(self):
        return self.total_price - self.deposit_paid

    def is_fully_paid(self):
        return self.payment_status == 'paid'

    def can_be_cancelled(self):
        return self.booking_status not in ['completed', 'cancelled']