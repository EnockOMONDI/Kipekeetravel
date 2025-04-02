from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    
    # Main image and gallery
    main_image = models.ImageField(upload_to='destinations/')
    gallery_image1 = models.ImageField(upload_to='destinations/gallery/', blank=True)
    gallery_image2 = models.ImageField(upload_to='destinations/gallery/', blank=True)
    gallery_image3 = models.ImageField(upload_to='destinations/gallery/', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Tour(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tours')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    group_size = models.IntegerField()
    languages = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, 
                               validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviews_count = models.IntegerField(default=0)
    
    # Tour-specific image
    main_image = models.ImageField(upload_to='tours/', blank=True)
    
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