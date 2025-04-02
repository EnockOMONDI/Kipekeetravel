from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Avg
from .models import Destination, Tour, Review
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class HomeView(ListView):
    model = Tour
    template_name = 'users/dede/index.html'
    context_object_name = 'tours'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_tours'] = Tour.objects.filter(rating__gte=4.5)[:6]
        context['popular_destinations'] = Destination.objects.all()[:6]
        return context

class TourListView(ListView):
    model = Tour
    template_name = 'users/dede/tour-grid-1.html'
    context_object_name = 'tours'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.all()
        return context

    def get_queryset(self):
        queryset = Tour.objects.all()
        destination = self.request.GET.get('destination')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        duration = self.request.GET.get('duration')

        if destination:
            queryset = queryset.filter(destination__slug=destination)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if duration:
            queryset = queryset.filter(duration=duration)

        return queryset.select_related('destination')  # Optimize database queries

class TourDetailView(DetailView):
    model = Tour
    template_name = 'users/dede/tour-details.html'
    context_object_name = 'tour'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.get_object()
        
        # Get reviews with aggregated ratings
        reviews = tour.reviews.all()
        avg_ratings = reviews.aggregate(
            avg_location=Avg('location_rating'),
            avg_price=Avg('price_rating'),
            avg_amenities=Avg('amenities_rating'),
            avg_services=Avg('services_rating'),
            avg_rooms=Avg('rooms_rating')
        )
        
        context.update({
            'reviews': reviews,
            'avg_ratings': avg_ratings,
            'highlights': tour.highlights.all(),
            'inclusions': tour.inclusions.all(),
            'tour_days': tour.tour_days.all(),
            'related_tours': Tour.objects.filter(destination=tour.destination).exclude(id=tour.id)[:3]
        })
        
        return context

def submit_review(request, tour_slug):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, slug=tour_slug)
        
        review = Review(
            tour=tour,
            user_name=request.POST.get('name'),
            rating=request.POST.get('rating'),
            comment=request.POST.get('message'),
            location_rating=request.POST.get('location_rating'),
            price_rating=request.POST.get('price_rating'),
            amenities_rating=request.POST.get('amenities_rating'),
            services_rating=request.POST.get('services_rating'),
            rooms_rating=request.POST.get('rooms_rating')
        )
        review.save()
        
        # Update tour rating and review count
        tour.reviews_count = tour.reviews.count()
        tour.rating = tour.reviews.aggregate(Avg('rating'))['rating__avg']
        tour.save()
        
        messages.success(request, 'Your review has been submitted successfully!')
        return redirect('dede:tour_detail', slug=tour_slug)
    
    return redirect('dede:tour_detail', slug=tour_slug)