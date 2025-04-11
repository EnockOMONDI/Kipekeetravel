from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from pyuploadcare.dj.models import ImageField
from django.utils import timezone
import random

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
    group_size = models.IntegerField()
    languages = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, 
                               validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviews_count = models.IntegerField(default=0)
    
    # Remove this line since we're using pyuploadcare's ImageField
    # main_image = models.ImageField(upload_to='tours/', blank=True)
    
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