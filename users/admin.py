from django.contrib import admin
from .models import UserBookings
from .models import Profile

# Register your models here.
admin.site.register(UserBookings)
admin.site.register(Profile)