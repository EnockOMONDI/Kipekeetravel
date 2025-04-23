from django.db import models
from django.utils.text import slugify
from pyuploadcare.dj.models import ImageField
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Event Categories"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Event(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    # Basic Event Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, related_name='events')
    description = models.TextField()
    main_image = ImageField(blank=True, null=True, manual_crop="16:9")
    
    # Event Details
    venue = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    
    # Event Status and Visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # Capacity and Registration
    max_capacity = models.PositiveIntegerField(help_text="Maximum number of attendees")
    registration_deadline = models.DateTimeField()
    
    # Additional Information
    website = models.URLField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    
    # Meta Information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'start_time']


class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100)  # e.g., VIP, Regular, Early Bird
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(help_text="Number of tickets available")
    
    # Sales Period
    sales_start = models.DateTimeField()
    sales_end = models.DateTimeField()
    
    # Additional Options
    max_tickets_per_order = models.PositiveIntegerField(default=10)
    min_tickets_per_order = models.PositiveIntegerField(default=1)


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    # Ticket Information
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='tickets')
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_tickets')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Purchase Information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    purchase_date = models.DateTimeField(auto_now_add=True)
    ticket_code = models.CharField(max_length=50, unique=True, blank=True)
    
    # Attendee Information
    attendee_name = models.CharField(max_length=200)
    attendee_email = models.EmailField()
    special_requirements = models.TextField(blank=True)


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = ImageField(manual_crop="16:9")
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class EventsLaunchNotification(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email

# Create your models here.
