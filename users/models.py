from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import BigAutoField
from pyuploadcare.dj.models import ImageField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = ImageField(null=True, blank=True, manual_crop="")
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'


class UserBookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey("adminside.Package", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    number_of_adults = models.PositiveIntegerField()
    number_of_children = models.PositiveIntegerField(blank=True, null=True)
    number_of_rooms = models.PositiveIntegerField(default=1)
    booking_date = models.DateField(auto_now_add=True)
    include_travelling = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True, null=True)
    paid=models.BooleanField(default=False)
    total_amount = models.PositiveIntegerField(default=0, blank=True, null=True)


    class Meta:
        ordering = ('-booking_date', )

    def __str__(self):
        return f"Booking for {self.full_name}  {self.package.package_name} on {self.booking_date}"