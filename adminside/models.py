from django.db import models
from django.contrib.auth.models import User
from users.models import UserBookings
from django.db.models import BigAutoField
from pyuploadcare.dj.models import ImageField

# Create your models here.

class Destination(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    dtn_description = models.TextField()
    Image = ImageField(blank=False, null=False, manual_crop="4:4")
    parent = models.ForeignKey(
        'self',  # Self-referential relationship
        on_delete=models.CASCADE,
        null=True, 
        blank=True, 
        related_name='sub_destinations'
    )

    def __str__(self):
        return f'{self.name}'
    
    def is_country(self):
        """Check if this destination is a country (has no parent)."""
        return self.parent is None



class Accomodation(models.Model):
    hotel_name = models.CharField(max_length=200)
    hotel_description = models.TextField()
    price_per_room = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.hotel_name}'

class Travel(models.Model):
    
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price_per_person = models.PositiveIntegerField()

    ## For Travelling Choices
    TRAIN = 'TN'
    FLIGHT = 'FT'
    BUS = 'BS'

    TRAVELLING_CHOICES = [
        (TRAIN, 'Train'),
        (FLIGHT, 'Flight'),
        (BUS, 'Bus')
    ]

    travelling_mode = models.CharField(max_length=2,choices=TRAVELLING_CHOICES,default=FLIGHT)

    def __str__(self):
        return f'{self.departure} to {self.arrival} | {self.travelling_mode}'



    
class Package(models.Model):
    main_destination = models.ForeignKey(
        Destination, 
        on_delete=models.CASCADE, 
        related_name='main_packages'
    )
    sub_destinations = models.ManyToManyField(
        Destination, 
        related_name='sub_packages', 
        blank=True
    )
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    accomodation = models.ForeignKey(Accomodation,on_delete=models.CASCADE)
    travel = models.ForeignKey(Travel,on_delete=models.CASCADE)
    bookings = models.ManyToManyField(User,through=UserBookings)
    Image = ImageField(blank=False, null=False, manual_crop="4:4",)
    package_name = models.CharField(max_length=200,default="NULL") # ye dalna
    adult_price = models.IntegerField()
    child_price = models.IntegerField() 
    description = models.TextField(default="NO DESCRIPTION ADDED")  
    inclusive = models.TextField()
    exclusive = models.TextField()
    number_of_days = models.PositiveIntegerField()
    number_of_times_booked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.package_name}'


class Itinerary(models.Model):
    package = models.OneToOneField(Package,on_delete=models.CASCADE,default=1)
    itinerary_name = models.CharField(max_length=200,default="NULL")

    def __str__(self):
        return f'{self.itinerary_name}'

class ItineraryDescription(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name='itinerarydescription_set', on_delete=models.CASCADE)    
    itinerary_description = models.TextField()
    day_number = models.IntegerField()
    
    class Meta:
        ordering = ['day_number']

    
    def __str__(self):
        return f'{self.itinerary.itinerary_name} | Day {self.day_number}'
    
  
