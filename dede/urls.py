from django.urls import path
from . import views

app_name = 'dede'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tours/', views.TourListView.as_view(), name='tour_list'),
    path('destination/<slug:slug>/', views.destination_detail, name='destination_detail'), 
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('tour/<slug:tour_slug>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('tour/<slug:tour_slug>/review/', views.submit_review, name='submit_review'),
    path('tour/<slug:tour_slug>/booking/', views.tour_booking, name='tour_booking'),
    path('daytrips/', views.DayTripListView.as_view(), name='daytrip_list'),
    path('daytrip/<slug:daytrip_slug>/', views.DayTripDetailView.as_view(), name='daytrip_detail'),
    path('daytrip/<slug:daytrip_slug>/book/', views.daytrip_booking, name='daytrip_booking'),
    path('daytrip/booking/confirmation/<str:booking_reference>/', views.daytrip_booking_confirmation, name='daytrip_booking_confirmation'),
    path('booking/confirmation/<str:booking_reference>/', views.booking_confirmation, name='booking_confirmation'),
]