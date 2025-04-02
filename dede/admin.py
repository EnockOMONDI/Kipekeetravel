from django.contrib import admin
from .models import Destination, Tour, TourHighlight, TourInclusion, TourDay, Review

class TourHighlightInline(admin.TabularInline):
    model = TourHighlight
    extra = 1

class TourInclusionInline(admin.TabularInline):
    model = TourInclusion
    extra = 1

class TourDayInline(admin.TabularInline):
    model = TourDay
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price', 'duration', 'rating', 'reviews_count')
    list_filter = ('destination', 'duration', 'rating')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TourHighlightInline, TourInclusionInline, TourDayInline, ReviewInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('destination', 'name', 'slug', 'description', 'price')
        }),
        ('Tour Details', {
            'fields': ('duration', 'group_size', 'languages', 'rating', 'reviews_count')
        }),
        ('Image', {
            'fields': ('main_image',)
        }),
    )

@admin.register(TourHighlight)
class TourHighlightAdmin(admin.ModelAdmin):
    list_display = ('tour', 'highlight')
    list_filter = ('tour',)
    search_fields = ('tour__name', 'highlight')

@admin.register(TourInclusion)
class TourInclusionAdmin(admin.ModelAdmin):
    list_display = ('tour', 'item', 'is_included')
    list_filter = ('tour', 'is_included')
    search_fields = ('tour__name', 'item')

@admin.register(TourDay)
class TourDayAdmin(admin.ModelAdmin):
    list_display = ('tour', 'day_number', 'title')
    list_filter = ('tour',)
    search_fields = ('tour__name', 'title', 'description')
    ordering = ('tour', 'day_number')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user_name', 'rating', 'created_at')
    list_filter = ('tour', 'rating', 'created_at')
    search_fields = ('tour__name', 'user_name', 'comment')
    readonly_fields = ('created_at',)